from fpdf import FPDF
from datetime import datetime
import io

class LombongoPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(108, 117, 125)
        self.cell(0, 10, "LombongoCare - Gestao Inteligente de Fluxo de Caixa", 0, 0, "L")
        self.cell(0, 10, f"Pagina {self.page_no()}", 0, 0, "R")

class PDFService:
    @staticmethod
    def gerar_extrato_pdf(user_name, receitas, despesas, total_receitas, total_despesas, saldo_atual):
        data_emissao = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        todas_transacoes = []
        for r in receitas:
            todas_transacoes.append({
                'data': r.get('data'), 'descricao': r.get('descricao'),
                'categoria': r.get('categoria'), 'tipo': 'receita', 'valor': float(r.get('valor', 0))
            })
        for d in despesas:
            todas_transacoes.append({
                'data': d.get('data'), 'descricao': d.get('descricao'),
                'categoria': d.get('categoria'), 'tipo': 'despesa', 'valor': float(d.get('valor', 0))
            })
        todas_transacoes.sort(key=lambda x: x['data'], reverse=True)

        pdf = LombongoPDF()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()
        
        pdf.set_fill_color(33, 37, 41)
        pdf.rect(0, 0, 210, 38, "F")
        
        pdf.set_fill_color(255, 204, 0)
        pdf.rect(0, 38, 210, 2, "F")
        
        pdf.set_y(10)
        pdf.set_font("Helvetica", "B", 22)
        pdf.set_text_color(255, 204, 0)
        pdf.cell(110, 10, "LombongoCare", 0, 0, "L")
        
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(80, 10, "EXTRATO DE FLUXO DE CAIXA", 0, 1, "R")
        
        pdf.set_y(22)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(206, 212, 218)
        pdf.cell(110, 5, "Gestao Financeira Resiliente e Inteligente", 0, 0, "L")
        pdf.cell(80, 5, f"Emissao: {data_emissao}", 0, 1, "R")
        
        pdf.set_y(48)
        pdf.set_fill_color(250, 250, 250)
        pdf.set_draw_color(233, 236, 239)
        pdf.cell(190, 12, "", 1, 0, "L", True)
        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(40, 44, 48)
        pdf.text(15, 55, "Utilizador:")
        pdf.set_font("Helvetica", "", 10)
        pdf.text(37, 55, user_name)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.text(130, 55, "Moeda Corrente:")
        pdf.set_font("Helvetica", "", 10)
        pdf.text(162, 55, "Kwanza Angolano (Kz)")
        
        pdf.set_y(68)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(33, 37, 41)
        pdf.cell(190, 6, "BALANCO CONSOLIDADO DO PERIODO", 0, 1, "L")
        
        pdf.set_y(76)
        x_start = 10
        card_w = 60
        gap = 5
        
        pdf.set_fill_color(255, 253, 245)
        pdf.rect(x_start, 76, card_w, 18, "F")
        pdf.set_draw_color(255, 204, 0)
        pdf.line(x_start, 76, x_start, 94)
        pdf.set_text_color(108, 117, 125)
        pdf.set_font("Helvetica", "B", 8)
        pdf.text(x_start + 4, 82, "SALDO ATUAL")
        pdf.set_text_color(33, 37, 41)
        pdf.set_font("Helvetica", "B", 12)
        pdf.text(x_start + 4, 90, f"{saldo_atual:,.2f} Kz".replace(",", "X").replace(".", ",").replace("X", "."))
        
        pdf.set_fill_color(248, 255, 249)
        pdf.rect(x_start + card_w + gap, 76, card_w, 18, "F")
        pdf.set_draw_color(25, 135, 84)
        pdf.line(x_start + card_w + gap, 76, x_start + card_w + gap, 94)
        pdf.set_text_color(108, 117, 125)
        pdf.set_font("Helvetica", "B", 8)
        pdf.text(x_start + card_w + gap + 4, 82, "TOTAL ENTRADAS")
        pdf.set_text_color(25, 135, 84)
        pdf.set_font("Helvetica", "B", 12)
        pdf.text(x_start + card_w + gap + 4, 90, f"+{total_receitas:,.2f} Kz".replace(",", "X").replace(".", ",").replace("X", "."))
        
        pdf.set_fill_color(255, 250, 253)
        pdf.rect(x_start + (card_w * 2) + (gap * 2), 76, card_w, 18, "F")
        pdf.set_draw_color(220, 53, 69)
        pdf.line(x_start + (card_w * 2) + (gap * 2), 76, x_start + (card_w * 2) + (gap * 2), 94)
        pdf.set_text_color(108, 117, 125)
        pdf.set_font("Helvetica", "B", 8)
        pdf.text(x_start + (card_w * 2) + (gap * 2) + 4, 82, "TOTAL SAIDAS")
        pdf.set_text_color(220, 53, 69)
        pdf.set_font("Helvetica", "B", 12)
        pdf.text(x_start + (card_w * 2) + (gap * 2) + 4, 90, f"-{total_despesas:,.2f} Kz".replace(",", "X").replace(".", ",").replace("X", "."))
        
        pdf.set_y(102)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(33, 37, 41)
        pdf.cell(190, 6, "DISCRIMINACAO DOS FLUXOS LANCADOS", 0, 1, "L")
        pdf.ln(2)
        
        pdf.set_fill_color(33, 37, 41)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(25, 8, " DATA", 0, 0, "L", True)
        pdf.cell(75, 8, " DESCRICAO", 0, 0, "L", True)
        pdf.cell(35, 8, " CATEGORIA", 0, 0, "L", True)
        pdf.cell(20, 8, " TIPO", 0, 0, "L", True)
        pdf.cell(35, 8, "VALOR ", 0, 1, "R", True)
        
        pdf.set_text_color(40, 44, 48)
        zebra = False
        for t in todas_transacoes:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_fill_color(248, 249, 250) if zebra else pdf.set_fill_color(255, 255, 255)
            
            pdf.cell(25, 8, f" {t['data']}", 0, 0, "L", True)
            
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(75, 8, f" {t['descricao']}", 0, 0, "L", True)
            
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(35, 8, f" {t['categoria']}", 0, 0, "L", True)
            
            if t['tipo'] == 'receita':
                pdf.set_text_color(25, 135, 84)
                pdf.cell(20, 8, " Entrada", 0, 0, "L", True)
                pdf.set_font("Helvetica", "B", 9)
                valor_str = f"+{t['valor']:,.2f} Kz"
            else:
                pdf.set_text_color(220, 53, 69)
                pdf.cell(20, 8, " Saida", 0, 0, "L", True)
                pdf.set_font("Helvetica", "B", 9)
                valor_str = f"-{t['valor']:,.2f} Kz"
                
            valor_pt = valor_str.replace(",", "X").replace(".", ",").replace("X", ".")
            pdf.cell(35, 8, f"{valor_pt} ", 0, 1, "R", True)
            pdf.set_text_color(40, 44, 48)
            
            pdf.set_draw_color(233, 236, 239)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            zebra = not zebra
            
        return bytes(pdf.output())