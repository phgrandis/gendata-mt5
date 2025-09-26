#!/usr/bin/env python3
"""
Script de Validação da Estrutura do Projeto Cérebro Local
Execute este script na raiz do seu projeto para diagnóstico completo
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any

class ProjetoValidator:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.report = {
            "estrutura": {},
            "docker": {},
            "python": {},
            "configuracoes": {},
            "problemas": [],
            "recomendacoes": []
        }
    
    def validate_structure(self):
        """Valida estrutura de diretórios e arquivos essenciais"""
        print("🔍 Validando estrutura do projeto...")
        
        # Arquivos esperados na raiz
        expected_root_files = [
            "docker-compose.yml", "docker-compose.yaml",
            "Dockerfile", "requirements.txt", "README.md",
            ".env", ".env.example", "pyproject.toml"
        ]
        
        found_files = []
        for file in expected_root_files:
            if (self.project_root / file).exists():
                found_files.append(file)
        
        self.report["estrutura"]["arquivos_raiz"] = found_files
        
        # Diretórios esperados
        expected_dirs = ["app", "src", "database", "db", "scripts", "docs", "config"]
        found_dirs = []
        
        for dir_name in expected_dirs:
            if (self.project_root / dir_name).is_dir():
                found_dirs.append(dir_name)
        
        self.report["estrutura"]["diretorios"] = found_dirs
        
        # Mapear toda estrutura
        structure = self._map_directory_structure(self.project_root)
        self.report["estrutura"]["mapa_completo"] = structure
        
        return found_files, found_dirs
    
    def validate_docker(self):
        """Valida configurações Docker"""
        print("🐳 Validando configurações Docker...")
        
        # Verificar Docker Compose
        compose_files = ["docker-compose.yml", "docker-compose.yaml"]
        compose_found = None
        
        for file in compose_files:
            if (self.project_root / file).exists():
                compose_found = file
                break
        
        if compose_found:
            self.report["docker"]["compose_file"] = compose_found
            try:
                # Tentar validar sintaxe do compose
                result = subprocess.run(
                    ["docker-compose", "-f", compose_found, "config"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                self.report["docker"]["compose_valid"] = result.returncode == 0
                if result.returncode != 0:
                    self.report["problemas"].append(f"Docker Compose inválido: {result.stderr}")
            except FileNotFoundError:
                self.report["problemas"].append("Docker Compose não instalado")
        
        # Verificar Dockerfiles
        dockerfiles = list(self.project_root.rglob("Dockerfile*"))
        self.report["docker"]["dockerfiles"] = [str(f.relative_to(self.project_root)) for f in dockerfiles]
        
        # Status do Docker
        try:
            result = subprocess.run(["docker", "version"], capture_output=True, text=True)
            self.report["docker"]["docker_installed"] = result.returncode == 0
        except FileNotFoundError:
            self.report["docker"]["docker_installed"] = False
            self.report["problemas"].append("Docker não instalado")
    
    def validate_python(self):
        """Valida configurações Python"""
        print("🐍 Validando configurações Python...")
        
        # Verificar requirements.txt
        req_files = ["requirements.txt", "pyproject.toml", "Pipfile"]
        found_req = []
        
        for req_file in req_files:
            if (self.project_root / req_file).exists():
                found_req.append(req_file)
        
        self.report["python"]["dependency_files"] = found_req
        
        # Ler requirements.txt se existir
        if "requirements.txt" in found_req:
            try:
                with open(self.project_root / "requirements.txt", "r") as f:
                    requirements = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
                self.report["python"]["requirements"] = requirements
            except Exception as e:
                self.report["problemas"].append(f"Erro lendo requirements.txt: {e}")
        
        # Encontrar arquivos Python
        py_files = list(self.project_root.rglob("*.py"))
        self.report["python"]["python_files"] = [str(f.relative_to(self.project_root)) for f in py_files]
        
        # Verificar virtual environment
        venv_indicators = [".venv", "venv", "env", ".virtualenv"]
        venv_found = any((self.project_root / venv).exists() for venv in venv_indicators)
        self.report["python"]["virtual_env"] = venv_found
        
        if not venv_found:
            self.report["recomendacoes"].append("Considere criar um ambiente virtual Python")
    
    def validate_configs(self):
        """Valida arquivos de configuração"""
        print("⚙️ Validando configurações...")
        
        config_files = [".env", ".env.example", "config.yml", "config.json", "settings.py"]
        found_configs = []
        
        for config_file in config_files:
            if (self.project_root / config_file).exists():
                found_configs.append(config_file)
        
        self.report["configuracoes"]["arquivos"] = found_configs
        
        # Verificar .env
        if ".env" in found_configs:
            try:
                with open(self.project_root / ".env", "r") as f:
                    env_vars = [line.split("=")[0] for line in f.readlines() 
                              if "=" in line and not line.startswith("#")]
                self.report["configuracoes"]["env_vars"] = env_vars
            except Exception as e:
                self.report["problemas"].append(f"Erro lendo .env: {e}")
    
    def _map_directory_structure(self, path: Path, max_depth: int = 3, current_depth: int = 0) -> Dict:
        """Mapeia estrutura de diretórios"""
        if current_depth > max_depth:
            return {}
        
        structure = {}
        try:
            for item in path.iterdir():
                if item.name.startswith('.') and item.name not in ['.env', '.env.example']:
                    continue
                
                if item.is_dir():
                    structure[f"{item.name}/"] = self._map_directory_structure(
                        item, max_depth, current_depth + 1
                    )
                else:
                    structure[item.name] = f"arquivo ({item.stat().st_size} bytes)"
        except PermissionError:
            structure["[ERRO]"] = "Sem permissão de leitura"
        
        return structure
    
    def generate_recommendations(self):
        """Gera recomendações baseadas na análise"""
        print("💡 Gerando recomendações...")
        
        # Recomendações baseadas na estrutura
        if not self.report["estrutura"]["arquivos_raiz"]:
            self.report["recomendacoes"].append("Projeto parece vazio - iniciar estrutura básica")
        
        if "docker-compose.yml" not in self.report["estrutura"]["arquivos_raiz"]:
            self.report["recomendacoes"].append("Adicionar docker-compose.yml para containerização")
        
        if "README.md" not in self.report["estrutura"]["arquivos_raiz"]:
            self.report["recomendacoes"].append("Adicionar README.md com documentação")
        
        if not self.report["python"]["dependency_files"]:
            self.report["recomendacoes"].append("Adicionar requirements.txt ou pyproject.toml")
        
        # Recomendações de segurança
        if ".env" in self.report["estrutura"]["arquivos_raiz"] and ".env.example" not in self.report["estrutura"]["arquivos_raiz"]:
            self.report["recomendacoes"].append("Criar .env.example para template de configuração")
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Executa validação completa"""
        print("🚀 Iniciando validação completa do projeto...\n")
        
        self.validate_structure()
        self.validate_docker()
        self.validate_python()
        self.validate_configs()
        self.generate_recommendations()
        
        return self.report
    
    def print_report(self):
        """Imprime relatório formatado"""
        print("\n" + "="*60)
        print("📋 RELATÓRIO DE VALIDAÇÃO DO PROJETO")
        print("="*60)
        
        # Estrutura
        print(f"\n📁 ESTRUTURA:")
        print(f"  Arquivos na raiz: {len(self.report['estrutura']['arquivos_raiz'])}")
        for file in self.report["estrutura"]["arquivos_raiz"]:
            print(f"    ✓ {file}")
        
        print(f"  Diretórios: {len(self.report['estrutura']['diretorios'])}")
        for dir_name in self.report["estrutura"]["diretorios"]:
            print(f"    ✓ {dir_name}/")
        
        # Docker
        print(f"\n🐳 DOCKER:")
        print(f"  Docker instalado: {'✓' if self.report['docker'].get('docker_installed') else '✗'}")
        print(f"  Compose válido: {'✓' if self.report['docker'].get('compose_valid') else '✗'}")
        print(f"  Dockerfiles encontrados: {len(self.report['docker'].get('dockerfiles', []))}")
        
        # Python
        print(f"\n🐍 PYTHON:")
        print(f"  Arquivos Python: {len(self.report['python'].get('python_files', []))}")
        print(f"  Dependências: {len(self.report['python'].get('dependency_files', []))}")
        print(f"  Virtual env: {'✓' if self.report['python'].get('virtual_env') else '✗'}")
        
        # Problemas
        if self.report["problemas"]:
            print(f"\n⚠️ PROBLEMAS ENCONTRADOS:")
            for problema in self.report["problemas"]:
                print(f"    • {problema}")
        
        # Recomendações
        if self.report["recomendacoes"]:
            print(f"\n💡 RECOMENDAÇÕES:")
            for rec in self.report["recomendacoes"]:
                print(f"    • {rec}")
        
        print(f"\n🎯 RESUMO:")
        score = self._calculate_score()
        print(f"    Score do projeto: {score}/100")
        print(f"    Status: {self._get_status(score)}")
        print("\n" + "="*60)
    
    def _calculate_score(self) -> int:
        """Calcula score do projeto (0-100)"""
        score = 0
        
        # Estrutura básica (30 pontos)
        if self.report["estrutura"]["arquivos_raiz"]:
            score += 15
        if self.report["estrutura"]["diretorios"]:
            score += 15
        
        # Docker (25 pontos)
        if self.report["docker"].get("docker_installed"):
            score += 10
        if self.report["docker"].get("compose_valid"):
            score += 15
        
        # Python (25 pontos)
        if self.report["python"].get("python_files"):
            score += 15
        if self.report["python"].get("dependency_files"):
            score += 10
        
        # Configurações (20 pontos)
        if self.report["configuracoes"]["arquivos"]:
            score += 20
        
        # Penalizar problemas
        score -= min(len(self.report["problemas"]) * 5, 30)
        
        return max(0, min(100, score))
    
    def _get_status(self, score: int) -> str:
        """Retorna status baseado no score"""
        if score >= 80:
            return "🟢 Excelente - Pronto para desenvolvimento"
        elif score >= 60:
            return "🟡 Bom - Algumas melhorias necessárias"
        elif score >= 40:
            return "🟠 Regular - Precisa de ajustes"
        else:
            return "🔴 Crítico - Requer reestruturação"

if __name__ == "__main__":
    # Permitir especificar diretório do projeto
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    validator = ProjetoValidator(project_path)
    report = validator.run_full_validation()
    validator.print_report()
    
    # Salvar relatório JSON
    with open("validacao_projeto.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Relatório detalhado salvo em: validacao_projeto.json")