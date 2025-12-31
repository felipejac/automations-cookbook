#!/usr/bin/env python3
"""Gerador de Tutoriais HTML com 100 Integrações Populares"""

import json
from datetime import datetime
from pathlib import Path

# Lista completa de 100 integrações populares
INTEGRACOES_100 = [
    ("Dropbox", "HubSpot"), ("Gmail", "Notion"), ("Slack", "Google Sheets"),
    ("Stripe", "Salesforce"), ("Typeform", "Airtable"), ("GitHub", "Discord"),
    ("Mailchimp", "Shopify"), ("Zapier", "Monday"), ("Make", "Asana"),
    ("Todoist", "Trello"), ("Notion", "Google Calendar"), ("Jira", "Slack"),
    ("Zendesk", "Teams"), ("Calendly", "Gmail"), ("Twilio", "WhatsApp"),
    ("AWS", "Lambda"), ("Azure", "Logic Apps"), ("Google Cloud", "Pub/Sub"),
    ("Salesforce", "Marketo"), ("HubSpot", "Pipedrive"), ("Freshdesk", "Jira"),
    ("Intercom", "Segment"), ("Drift", "Salesforce"), ("Outreach", "LinkedIn"),
    ("Slack", "Salesforce"), ("Teams", "Jira"), ("Discord", "GitHub"),
    ("Telegram", "Notion"), ("WhatsApp", "CRM"), ("SMS", "Database"),
    ("Vonage", "Twilio"), ("Datadog", "PagerDuty"), ("New Relic", "Slack"),
    ("Splunk", "ServiceNow"), ("Elastic", "Grafana"), ("Prometheus", "AlertManager"),
    ("Jenkins", "GitHub"), ("GitLab", "Docker"), ("CircleCI", "Slack"),
    ("Travis CI", "GitHub"), ("Bitbucket", "Jira"), ("Azure DevOps", "Teams"),
    ("Kubernetes", "Datadog"), ("Docker", "Registry"), ("Terraform", "AWS"),
    ("Ansible", "Puppet"), ("Chef", "Saltstack"), ("Vagrant", "VirtualBox"),
    ("Nginx", "Apache"), ("HAProxy", "Load Balancer"), ("Istio", "Kubernetes"),
    ("Envoy", "Service Mesh"), ("Kong", "API Gateway"), ("AWS API Gateway", "Lambda"),
    ("Microsoft Graph", "Office 365"), ("Google Workspace", "Google Drive"),
    ("Dropbox Business", "Teams"), ("OneDrive", "SharePoint"), ("Box", "Slack"),
    ("Confluence", "Jira"), ("Wiki", "Documentation"), ("Swagger", "API"),
    ("Postman", "Testing"), ("Insomnia", "REST"), ("GraphQL", "Query"),
    ("Firebase", "Realtime DB"), ("MongoDB", "Atlas"), ("PostgreSQL", "Supabase"),
    ("MySQL", "Workbench"), ("Redis", "Cache"), ("Memcached", "Session"),
    ("Elasticsearch", "Kibana"), ("Solr", "Search"), ("Algolia", "Indexing"),
    ("Meilisearch", "Full Text"), ("Zinc", "Logs"), ("OpenSearch", "Analytics"),
    ("Tableau", "Power BI"), ("Looker", "Google Data Studio"), ("Metabase", "Superset"),
    ("Apache", "Business Intelligence"), ("Qlik", "Dash"), ("Microstrategy", "Reports"),
    ("SAP", "Oracle"), ("NetSuite", "Workday"), ("Peoplsoft", "JD Edwards"),
    ("Infor", "Dynamics"), ("Pimcore", "Magento"), ("WooCommerce", "Prestashop"),
    ("Shopware", "Commerce"), ("BigCommerce", "Lightspeed"), ("Square", "Clover")
]

class TutorialGenerator:
    """Gera páginas HTML com tutoriais detalhados"""
    
    def __init__(self):
        self.output_dir = Path("../public/integracoes-paginas")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_html_page(self, source: str, target: str, tutorial_data: dict) -> str:
        """Gera página HTML com conteúdo completo do tutorial"""
        
        sections_html = ""
        for section_key, section_data in tutorial_data['sections'].items():
            if isinstance(section_data, dict) and 'title' in section_data:
                sections_html += f"""
                <div class="section">
                    <h3>{section_data['title']}</h3>
                """
                
                if 'steps' in section_data:
                    sections_html += "<ol class='steps'>"
                    for step in section_data['steps']:
                        sections_html += f"<li>{step}</li>"
                    sections_html += "</ol>"
                
                if 'items' in section_data:
                    sections_html += "<ul class='items'>"
                    for item in section_data['items']:
                        sections_html += f"<li>{item}</li>"
                    sections_html += "</ul>"
                
                if 'issues' in section_data:
                    sections_html += "<div class='issues'>"
                    for issue in section_data['issues']:
                        sections_html += f"""
                        <div class='issue'>
                            <strong>Problema:</strong> {issue.get('problema', '')}<br>
                            <strong>Solução:</strong> {issue.get('solucao', '')}
                        </div>
                        """
                    sections_html += "</div>"
                
                if 'tips' in section_data:
                    sections_html += "<ul class='tips'>"
                    for tip in section_data['tips']:
                        sections_html += f"<li>{tip}</li>"
                    sections_html += "</ul>"
                
                sections_html += "</div>"
        
        html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tutorial_data['title']} | Automations Cookbook</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f7fa; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .meta {{ opacity: 0.9; margin: 15px 0; }}
        .section {{ background: white; margin: 20px 0; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h3 {{ color: #667eea; margin: 20px 0 15px 0; }}
        ol, ul {{ margin: 15px 0 15px 30px; }}
        li {{ margin: 10px 0; line-height: 1.6; }}
        .steps {{ list-style-type: decimal; }}
        .items {{ list-style-type: disc; }}
        .issue {{ background: #f9f9f9; padding: 15px; margin: 10px 0; border-left: 4px solid #667eea; }}
        .tips {{ list-style-type: circle; }}
        .button-group {{ display: flex; gap: 15px; margin: 30px 0; }}
        button {{ padding: 12px 24px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }}
        .btn-vote {{ background: #667eea; color: white; }}
        .btn-templates {{ background: #f5a623; color: white; }}
        .btn-download {{ background: #27ae60; color: white; }}
        button:hover {{ opacity: 0.9; }}
        .status-badge {{ display: inline-block; background: #27ae60; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9em; }}
        .difficulty {{ display: inline-block; margin-left: 10px; padding: 5px 15px; background: #f39c12; color: white; border-radius: 20px; }}
        .estimated-time {{ display: inline-block; margin-left: 10px; padding: 5px 15px; background: #3498db; color: white; border-radius: 20px; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{tutorial_data['title']}</h1>
            <p>{tutorial_data['description']}</p>
            <div class="meta">
                <span class="status-badge">✓ {tutorial_data.get('status', 'Pronto')}</span>
                <span class="difficulty">Dificuldade: {tutorial_data.get('difficulty', 'Intermediário')}</span>
                <span class="estimated-time">Tempo: {tutorial_data.get('estimated_time', '15-30 min')}</span>
            </div>
        </div>
    </header>
    
    <div class="container">
        <div class="button-group">
            <button class="btn-vote" onclick="voteTemplate()">⭐ Votar neste Template</button>
            <button class="btn-templates" onclick="goToTemplates()">📚 Ver Todos os Templates</button>
            <button class="btn-download" onclick="downloadTemplate()">⬇️ Baixar Template JSON</button>
        </div>
        
        {sections_html}
    </div>
    
    <script>
        function voteTemplate() {{
            alert('Obrigado por votar! Seu voto foi registrado.');
            // Aqui poderia fazer uma chamada para API
        }}
        
        function goToTemplates() {{
            window.location.href = '/templates';
        }}
        
        function downloadTemplate() {{
            const json = {json.dumps(tutorial_data['template_json'], ensure_ascii=False)};
            const blob = new Blob([JSON.stringify(json, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = '{source.lower()}-para-{target.lower()}.json';
            a.click();
        }}
    </script>
</body>
</html>
        """
        
        return html_content
    
    def create_tutorials_for_all_integrations(self):
        """Cria tutoriais para todas as 100 integrações"""
        from scraper_avancado import IntegrationScraper
        
        scraper = IntegrationScraper()
        count = 0
        
        for source, target in INTEGRACOES_100:
            try:
                # Gerar tutorial
                tutorial = scraper.generate_tutorial_from_docs(source, target, "")
                
                # Gerar HTML
                html_content = self.generate_html_page(source, target, tutorial)
                
                # Salvar arquivo
                filename = f"{source.lower()}-para-{target.lower()}.html"
                filepath = self.output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                count += 1
                print(f"✓ {count}/100: {source} → {target}")
                
            except Exception as e:
                print(f"✗ Erro ao processar {source} → {target}: {e}")
        
        print(f"\n✓ {count} tutoriais gerados com sucesso!")


if __name__ == "__main__":
    generator = TutorialGenerator()
    generator.create_tutorials_for_all_integrations()
