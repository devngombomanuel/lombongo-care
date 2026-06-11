# Código estrutural embutido em app/services/pdf_service.py
from weasyprint import HTML
from datetime import datetime

class PDFService:
    @staticmethod
    def gerar_extrato_pdf(user_name, receitas, despesas, total_receitas, total_despesas, saldo_atual):
        """
        Gera um ficheiro PDF profissional utilizando o WeasyPrint baseado num template HTML.
        Retorna os bytes do PDF gerado.
        """
        data_emissao = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        # Consolidação e ordenação estável (Decrescente por Data)
        todas_transacoes = []
        for r in receitas:
            todas_transacoes.append({
                'data': r.get('data'), 'descricao': r.get('descricao'),
                'categoria': r.get('categoria'), 'periodicidade': r.get('periodicidade', 'unica'),
                'tipo': 'receita', 'valor': float(r.get('valor', 0))
            })
        for d in despesas:
            todas_transacoes.append({
                'data': d.get('data'), 'descricao': d.get('descricao'),
                'categoria': d.get('categoria'), 'periodicidade': d.get('periodicidade', 'unica'),
                'tipo': 'despesa', 'valor': float(d.get('valor', 0))
            })
        todas_transacoes.sort(key=lambda x: x['data'], reverse=True)

        # HTML Estruturado com CSS Paged Media (Identidade LombongoCare)
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @page {{
            size: A4;
            margin: 20mm 15mm 20mm 15mm;
            @bottom-right {{
                content: "Página " counter(page) " de " counter(pages);
                font-family: 'Arial', sans-serif; font-size: 8pt; color: #6c757d;
            }}
            @bottom-left {{
                content: "LombongoCare – Gestão Inteligente de Fluxo de Caixa";
                font-family: 'Arial', sans-serif; font-size: 8pt; color: #6c757d;
            }}
        }}
        *, *::before, *::after {{ box-sizing: border-box; }}
        body {{
            font-family: 'Arial', sans-serif; margin: 0; padding: 0;
            color: #282c30; font-size: 10pt; line-height: 1.4;
        }}
        /* Banner superior full-bleed usando margens negativas */
        .header-banner {{
            margin: -20mm -15mm 25px -15mm;
            padding: 25px 15mm;
            background-color: #212529;
            color: #ffffff;
            border-bottom: 5px solid #FFCC00;
        }}
        .header-table {{ width: 100%; border-collapse: collapse; }}
        .brand-title {{ font-size: 22pt; font-weight: bold; color: #FFCC00; margin: 0; }}
        .brand-subtitle {{ font-size: 9pt; color: #ced4da; margin: 2px 0 0 0; }}
        .doc-title {{ font-size: 14pt; font-weight: bold; text-transform: uppercase; text-align: right; margin: 0; }}
        .doc-meta {{ font-size: 8.5pt; color: #ced4da; text-align: right; margin: 4px 0 0 0; }}
        
        .client-info {{
            margin-bottom: 25px; background-color: #fafafa;
            border: 1px solid #e9ecef; border-radius: 6px; padding: 12px 15px;
        }}
        .kpi-container {{ width: 100%; margin-bottom: 30px; border-collapse: separate; border-spacing: 12px 0; margin-left: -12px; }}
        .kpi-card {{ background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 8px; padding: 12px 15px; vertical-align: middle; }}
        .kpi-saldo {{ border-left: 5px solid #FFCC00; background-color: #fffdf5; }}
        .kpi-receita {{ border-left: 5px solid #198754; background-color: #f8fff9; }}
        .kpi-despesa {{ border-left: 5px solid #dc3545; background-color: #fffafd; }}
        .kpi-label {{ font-size: 8pt; text-transform: uppercase; color: #6c757d; font-weight: bold; margin-bottom: 4px; }}
        .kpi-value {{ font-size: 14pt; font-weight: bold; color: #212529; }}
        
        h2 {{
            font-size: 12pt; font-weight: bold; color: #212529;
            border-left: 4px solid #FFCC00; padding-left: 8px;
            margin: 20px 0 12px 0; text-transform: uppercase; page-break-after: avoid;
        }}
        .data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        .data-table th {{ background-color: #212529; color: #ffffff; font-weight: bold; padding: 8px 10px; font-size: 9pt; text-transform: uppercase; }}
        .data-table td {{ padding: 8px 10px; border-bottom: 1px solid #dee2e6; font-size: 9pt; }}
        .data-table tr:nth-child(even) td {{ background-color: #fdfdfd; }}
        
        .badge {{ display: inline-block; padding: 2px 6px; font-size: 7.5pt; font-weight: bold; border-radius: 4px; text-transform: uppercase; }}
        .badge-receita {{ background-color: #e8f5e9; color: #198754; }}
        .badge-despesa {{ background-color: #ffebee; color: #dc3545; }}
        .badge-periodicidade {{ background-color: #f1f3f5; color: #495057; border: 1px solid #ced4da; }}
        .text-success {{ color: #198754 !important; }}
        .text-danger {{ color: #dc3545 !important; }}
        .text-right {{ text-align: right; }}
    </style>
</head>
<body>
    <div class="header-banner">
        <table class="header-table">
            <tr>
                <td>
                    <div class="brand-title">LombongoCare</div>
                    <div class="brand-subtitle">Gestão Financeira Resiliente e Inteligente</div>
                </td>
                <td>
                    <div class="doc-title">Extrato de Fluxo de Caixa</div>
                    <div class="doc-meta">Emissão: {data_emissao}</div>
                </td>
            </tr>
        </table>
    </div>

    <div class="client-info">
        <table style="width: 100%;">
            <tr>
                <td style="font-weight: bold; width: 12%;">Utilizador:</td>
                <td>{user_name}</td>
                <td style="font-weight: bold; width: 15%; text-align: right;">Moeda Corrente:</td>
                <td style="width: 22%; text-align: right; font-weight: bold;">Kwanza Angolano (Kz)</td>
            </tr>
        </table>
    </div>

    <h2>Balanço Consolidado do Período</h2>
    <table class="kpi-container">
        <tr>
            <td class="kpi-card kpi-saldo">
                <div class="kpi-label">Saldo Atual</div>
                <div class="kpi-value">{"%.2f" % saldo_atual} Kz</div>
            </td>
            <td class="kpi-card kpi-receita">
                <div class="kpi-label">Total Entradas</div>
                <div class="kpi-value text-success">+{"%.2f" % total_receitas} Kz</div>
            </td>
            <td class="kpi-card kpi-despesa">
                <div class="kpi-label">Total Saídas</div>
                <div class="kpi-value text-danger">-{"%.2f" % total_despesas} Kz</div>
            </td>
        </tr>
    </table>

    <h2>Discriminação dos Fluxos Lançados</h2>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 15%;">Data</th>
                <th style="width: 35%;">Descrição</th>
                <th style="width: 15%;">Categoria</th>
                <th style="width: 15%;">Periodicidade</th>
                <th style="width: 20%; text-align: right;">Valor</th>
            </tr>
        </thead>
        <tbody>
    '''
        for t in todas_transacoes:
            b_class = 'badge-receita' if t['tipo'] == 'receita' else 'badge-despesa'
            sinal = '+' if t['tipo'] == 'receita' else '-'
            t_class = 'text-success' if t['tipo'] == 'receita' else 'text-danger'
            html_content += f'''
            <tr>
                <td>{t['data']}</td>
                <td style="font-weight: 600;">{t['descricao']}</td>
                <td><span class="badge {b_class}">{t['categoria']}</span></td>
                <td><span class="badge badge-periodicidade">{t['periodicidade']}</span></td>
                <td class="{t_class} text-right" style="font-weight: bold;">{sinal}{"%.2f" % t['valor']} Kz</td>
            </tr>'''
            
        html_content += '''</tbody></table></body></html>'''
        return HTML(string=html_content).write_pdf()