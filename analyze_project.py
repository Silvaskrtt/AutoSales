import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import json

class ProjectStructureAnalyzer:
    def __init__(self, root_path: str = "."):
        """
        Inicializa o analisador de estrutura de projeto.
        
        Args:
            root_path: Caminho raiz do projeto (padrão: diretório atual)
        """
        self.root_path = Path(root_path).resolve()
        self.issues = []
        self.warnings = []
        self.structure = {}
        
        # Estruturas recomendadas para diferentes tipos de projeto
        self.recommended_structures = {
            "python": {
                "required_dirs": ["src", "tests", "docs"],
                "optional_dirs": ["scripts", "data", "config", "examples"],
                "required_files": ["setup.py", "README.md", "requirements.txt"],
                "optional_files": [".gitignore", "LICENSE", "Makefile", "pyproject.toml"],
                "patterns": {
                    "src": "**/*.py",
                    "tests": "test_*.py",
                    "docs": "*.md"
                }
            },
            "web": {
                "required_dirs": ["src", "public", "tests"],
                "optional_dirs": ["components", "styles", "assets", "config"],
                "required_files": ["package.json", "README.md", "index.html"],
                "optional_files": [".gitignore", "webpack.config.js", "vite.config.js"],
                "patterns": {
                    "src": ["**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx"],
                    "public": "**/*",
                    "tests": "**/*.test.js"
                }
            },
            "data_science": {
                "required_dirs": ["notebooks", "data", "src", "models", "reports"],
                "optional_dirs": ["config", "scripts", "tests"],
                "required_files": ["README.md", "requirements.txt", "environment.yml"],
                "optional_files": [".gitignore", "Makefile", "setup.py"],
                "patterns": {
                    "notebooks": "*.ipynb",
                    "data": ["raw/*", "processed/*", "interim/*"],
                    "src": "**/*.py",
                    "models": "*.pkl",
                    "reports": ["*.html", "*.pdf"]
                }
            }
        }
    
    def detect_project_type(self) -> str:
        """
        Tenta detectar automaticamente o tipo do projeto baseado nos arquivos presentes.
        
        Returns:
            str: Tipo do projeto detectado ('python', 'web', 'data_science' ou 'unknown')
        """
        files = list(self.root_path.rglob("*"))
        
        # Verificar padrões para cada tipo de projeto
        if any(f.name == "setup.py" for f in files) or any(f.name == "requirements.txt" for f in files):
            return "python"
        elif any(f.name == "package.json" for f in files):
            return "web"
        elif any(f.name == "environment.yml" for f in files) or any("notebooks" in str(f) for f in files):
            return "data_science"
        
        # Verificar extensões comuns
        extensions = {f.suffix for f in files if f.suffix}
        if ".py" in extensions and ".ipynb" in extensions:
            return "data_science"
        elif ".js" in extensions or ".ts" in extensions:
            return "web"
        elif ".py" in extensions:
            return "python"
        
        return "unknown"
    
    def scan_project(self) -> Dict:
        """
        Escaneia a estrutura atual do projeto.
        
        Returns:
            Dict: Estrutura do projeto em formato de árvore
        """
        self.structure = self._build_tree(self.root_path)
        return self.structure
    
    def _build_tree(self, path: Path, max_depth: int = 3, current_depth: int = 0) -> Dict:
        """
        Constrói uma representação em árvore da estrutura de diretórios.
        
        Args:
            path: Caminho atual
            max_depth: Profundidade máxima de escaneamento
            current_depth: Profundidade atual
            
        Returns:
            Dict: Representação em árvore
        """
        if current_depth >= max_depth:
            return {"...": "max depth reached"}
        
        tree = {}
        try:
            for item in sorted(path.iterdir()):
                if item.name.startswith(('.', '__pycache__', 'node_modules')):
                    continue  # Ignorar arquivos/diretórios ocultos e caches
                
                if item.is_dir():
                    tree[item.name] = self._build_tree(item, max_depth, current_depth + 1)
                else:
                    if item.name not in tree:
                        tree[item.name] = None
        except PermissionError:
            tree["ERROR"] = "Permission denied"
        
        return tree
    
    def validate_structure(self, project_type: str = None) -> Tuple[List[str], List[str]]:
        """
        Valida a estrutura do projeto contra as recomendações.
        
        Args:
            project_type: Tipo de projeto para validar (se None, detecta automaticamente)
            
        Returns:
            Tuple[List[str], List[str]]: Listas de problemas e avisos
        """
        if project_type is None:
            project_type = self.detect_project_type()
        
        self.issues = []
        self.warnings = []
        
        if project_type == "unknown":
            self.warnings.append("Não foi possível determinar o tipo do projeto automaticamente")
            return self.issues, self.warnings
        
        if project_type not in self.recommended_structures:
            self.issues.append(f"Tipo de projeto '{project_type}' não suportado")
            return self.issues, self.warnings
        
        rules = self.recommended_structures[project_type]
        
        # Verificar diretórios obrigatórios
        for required_dir in rules["required_dirs"]:
            if not (self.root_path / required_dir).exists():
                self.issues.append(f"Diretório obrigatório ausente: '{required_dir}/'")
        
        # Verificar arquivos obrigatórios
        for required_file in rules["required_files"]:
            if not (self.root_path / required_file).exists():
                self.issues.append(f"Arquivo obrigatório ausente: '{required_file}'")
        
        # Verificar diretórios opcionais (apenas aviso)
        for optional_dir in rules["optional_dirs"]:
            if not (self.root_path / optional_dir).exists():
                self.warnings.append(f"Diretório recomendado ausente: '{optional_dir}/'")
        
        # Verificar arquivos opcionais (apenas aviso)
        for optional_file in rules["optional_files"]:
            if not (self.root_path / optional_file).exists():
                self.warnings.append(f"Arquivo recomendado ausente: '{optional_file}'")
        
        return self.issues, self.warnings
    
    def generate_report(self, project_type: str = None) -> str:
        """
        Gera um relatório detalhado da análise.
        
        Args:
            project_type: Tipo de projeto para validar
            
        Returns:
            str: Relatório formatado
        """
        if project_type is None:
            project_type = self.detect_project_type()
        
        issues, warnings = self.validate_structure(project_type)
        
        report = []
        report.append("=" * 60)
        report.append(f"RELATÓRIO DE ANÁLISE DE ESTRUTURA DO PROJETO")
        report.append("=" * 60)
        report.append(f"\nProjeto analisado: {self.root_path}")
        report.append(f"Tipo detectado: {project_type.upper()}")
        report.append("-" * 60)
        
        # Mostrar estrutura atual
        report.append("\nESTRUTURA ATUAL DO PROJETO:")
        report.append(self._format_tree(self.structure))
        
        # Mostrar problemas
        report.append("\n" + "-" * 60)
        report.append("PROBLEMAS ENCONTRADOS:")
        if issues:
            for i, issue in enumerate(issues, 1):
                report.append(f"  {i}. ❌ {issue}")
        else:
            report.append("  ✅ Nenhum problema crítico encontrado!")
        
        # Mostrar avisos
        report.append("\nAVISOS E RECOMENDAÇÕES:")
        if warnings:
            for i, warning in enumerate(warnings, 1):
                report.append(f"  {i}. ⚠️ {warning}")
        else:
            report.append("  ✅ Nenhum aviso para reportar!")
        
        # Sugestões de melhoria
        report.append("\n" + "-" * 60)
        report.append("SUGESTÕES DE MELHORIA:")
        
        if project_type in self.recommended_structures:
            rules = self.recommended_structures[project_type]
            
            # Sugerir diretórios que poderiam ser criados
            missing_important = []
            for d in rules["required_dirs"] + rules["optional_dirs"]:
                if not (self.root_path / d).exists():
                    missing_important.append(d)
            
            if missing_important:
                report.append("  Considere criar os seguintes diretórios:")
                for d in missing_important[:5]:  # Limitar a 5 sugestões
                    report.append(f"    - {d}/")
            else:
                report.append("  ✅ Estrutura de diretórios parece adequada!")
            
            # Sugerir arquivos importantes
            missing_files = []
            for f in rules["required_files"] + rules["optional_files"]:
                if not (self.root_path / f).exists():
                    missing_files.append(f)
            
            if missing_files:
                report.append("\n  Considere adicionar os seguintes arquivos:")
                for f in missing_files[:5]:  # Limitar a 5 sugestões
                    report.append(f"    - {f}")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)
    
    def _format_tree(self, tree: Dict, indent: str = "") -> str:
        """
        Formata a árvore de diretórios para exibição.
        
        Args:
            tree: Dicionário representando a árvore
            indent: Indentação atual
            
        Returns:
            str: Árvore formatada
        """
        result = []
        for name, content in tree.items():
            if content is None:
                result.append(f"{indent}📄 {name}")
            elif isinstance(content, dict):
                if content:
                    result.append(f"{indent}📁 {name}/")
                    result.append(self._format_tree(content, indent + "  "))
                else:
                    result.append(f"{indent}📁 {name}/ (vazio)")
        return "\n".join(result)
    
    def export_json(self, output_file: str = "project_structure.json"):
        """
        Exporta a estrutura do projeto para um arquivo JSON.
        
        Args:
            output_file: Nome do arquivo de saída
        """
        data = {
            "root": str(self.root_path),
            "structure": self.structure,
            "issues": self.issues,
            "warnings": self.warnings,
            "project_type": self.detect_project_type()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Estrutura exportada para {output_file}")

def main():
    """
    Função principal para execução do script.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Analisa a estrutura de um projeto')
    parser.add_argument('path', nargs='?', default='.', help='Caminho do projeto (padrão: diretório atual)')
    parser.add_argument('--type', choices=['python', 'web', 'data_science', 'auto'], 
                       default='auto', help='Tipo de projeto (padrão: auto-detect)')
    parser.add_argument('--export', help='Exportar estrutura para arquivo JSON')
    
    args = parser.parse_args()
    
    # Criar analisador
    analyzer = ProjectStructureAnalyzer(args.path)
    
    print(f"\n🔍 Analisando projeto em: {analyzer.root_path}")
    print("Escaneando estrutura...")
    
    # Escanear projeto
    analyzer.scan_project()
    
    # Determinar tipo de projeto
    project_type = args.type
    if project_type == 'auto':
        project_type = analyzer.detect_project_type()
    
    # Gerar e mostrar relatório
    report = analyzer.generate_report(project_type)
    print(report)
    
    # Exportar se solicitado
    if args.export:
        analyzer.export_json(args.export)
    
    # Retornar código de erro se houver problemas críticos
    if analyzer.issues:
        sys.exit(1)

if __name__ == "__main__":
    main()