from odoo import models, fields, api, _

class SevendCorrespondence(models.Model):
    _name = 'sevend.correspondence'
    _description = 'Yazışmalar'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Referans ID', required=True, copy=False, readonly=True, default='Yeni')
    type = fields.Selection([
        ('incoming', 'Gelen'),
        ('outgoing', 'Giden')
    ], string='Yazı Tipi', default='incoming', required=True)
    
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('sent', 'Gönderildi / Teslim Alındı'),
        ('replied', 'Cevaplandı'),
        ('archived', 'Arşivlendi')
    ], string='Durum', default='draft', tracking=True)

    project_code = fields.Char(string='Proje Kod')
    series = fields.Char(string='Yazı Seri')
    department = fields.Char(string='Departman')
    document_number = fields.Char(string='Belge No')
    branch = fields.Char(string='Şube')
    date = fields.Date(string='Tarih', default=fields.Date.today)
    
    # Alıcı / Gönderici Bilgileri
    recipient_name = fields.Char(string='Kime İsim')
    recipient_address = fields.Text(string='Kime Adres')
    recipient_email = fields.Char(string='Gönderilecek Mail Adresi')
    cc_list = fields.Char(string='CC Liste')
    
    # Konu ve İçerik (TR/EN)
    subject = fields.Char(string='Konu')
    subject_en = fields.Char(string='Konu EN')
    content = fields.Html(string='İçerik')
    content_en = fields.Html(string='İçerik EN')
    content_2 = fields.Html(string='İçerik 2')
    content_2_en = fields.Html(string='İçerik 2 EN')
    
    # İmza / Ünvan
    full_name = fields.Char(string='Ad Soyad')
    job_title = fields.Char(string='Ünvan')
    job_title_en = fields.Char(string='Ünvan EN')
    
    # İlgi Listesi (Reference List)
    reference_ids = fields.Many2many('sevend.correspondence', 'correspondence_reference_rel', 
                                     'src_id', 'dest_id', string='İlgi Listesi')
    reference_text = fields.Text(string='İlgi Listesi Metin')
    reference_text_en = fields.Text(string='İlgi Listesi EN')
    
    # Teknik / Linkler
    is_mail_sent = fields.Boolean(string='E-Mail Gönderildi mi?', default=False)
    sharepoint_link = fields.Char(string='Sharepoint Link')
    test_counter = fields.Integer(string='Test Sayacı')
    pdf_url = fields.Char(string='PDF URL')
    visual = fields.Binary(string='Görsel / Belge')

    @api.model
    def create(self, vals):
        if vals.get('name', 'Yeni') == 'Yeni':
            vals['name'] = self.env['ir.sequence'].next_by_code('sevend.correspondence') or 'Yeni'
        return super(SevendCorrespondence, self).create(vals)

    def action_send_mail(self):
        """ E-Mail gönderme butonu için placeholder """
        self.ensure_one()
        self.is_mail_sent = True
        return True
