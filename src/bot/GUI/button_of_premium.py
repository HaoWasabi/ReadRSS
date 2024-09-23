import datetime
import os
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ui import View, Button

from .embed_custom import EmbedCustom

from ..utils.create_qr_payment import QRGenerator

from ..BLL import QrPayCodeBLL
from ..DTO import PremiumDTO, QrPayCodeDTO


class ButtonOfPremium(Button):
    def __init__(self, pre: PremiumDTO, cls):
        super().__init__(label=pre.premium_name)
        self.pre = pre
        self.cls = cls

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()

        embed_text = EmbedCustom(
            id_server=str(interaction.guild.id) if interaction.guild else "DM",
            title="Nạp để mở gói premium",
            description="Gói premium mang đến nhiều tính năng hơn")

        embed_text.add_field(
            name="Ngân hàng MB-Bank", value=os.getenv('BANK_USER_NAME'), inline=False)
        embed_text.add_field(name="Số Tiền:", value=f"{
                             self.pre.price}đ", inline=False)

        if (interaction.guild is None or interaction.channel is None):
            await interaction.send('có gì đó lạ lắm')
            return

        qr_id = QRGenerator.generator_id()
        embed_text.add_field(name="Nội dung:",
                             value=f"T{qr_id}T",
                             inline=False)

        embed_text.set_image(QRGenerator.generator_qr(
            qr_id, int(self.pre.price)))

        message = await interaction.edit_original_message(content='', embed=embed_text, view=None)

        if message is None:
            await interaction.send('có gì đó lạ lắm')
            return

        qr = QrPayCodeDTO(qr_id, str(interaction.user.id), str(  # type: ignore
            message.channel.id), self.pre.premium_id, str(message.id), datetime.datetime.now(), False)

        qr_pay_code_bll = QrPayCodeBLL()
        qr_pay_code_bll.insert_qr_pay_code(qr)
        if not self.cls.start_listener_bank_history.is_running():
            self.cls.start_listener_bank_history.start()
        self.cls.start_time = datetime.datetime.now()
