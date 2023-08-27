import sqlite3
import traceback
import discord
from discord.ui import View, Select, button

tag_name_list = ['еда', 'холодное оружие', 'метательное оружие', 'огнестрельное оружие', 'броня', 'одежда', 'дерево', 'камень', 'драгоценности', 'материалы']

async def delete_by_id(interaction, id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    delete_query = f"DELETE FROM Prices WHERE id = {id}"

    try:
        cursor.execute(delete_query)
        conn.commit()
        await interaction.response.send_message(f"Предмет под номером {id} был удалён", ephemeral = True)
    except sqlite3.Error as e:
        await interaction.response.send_message(f"Ошибка удаления: {e}", ephemeral = True)
    finally:
        conn.close()

class TagChoose(Select):
    def __init__(self, id, name, desc, price, tag_name_list, action):
        options = [discord.SelectOption(label=x) for x in tag_name_list]
        super().__init__(placeholder="Выберите тег. По умолчанию: Еда.", min_values=1, max_values=1, options=options)
        self.name = name
        self.desc = desc
        self.price = price
        self.action = action
        self.tag_name_list = tag_name_list
        self.id = id

    async def callback(self, interaction: discord.Interaction):
        tag = self.values[0]  # Changed from `valuesp` to `values`
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Prices (
            id REAL,
            product TEXT,
            tag TEXT,
            description TEXT,
            price REAL
        )''')
        if self.action == "add":
            cursor.execute('SELECT MAX(id) FROM Prices')
            highest_id = cursor.fetchone()[0]
            new_id = highest_id + 1 if highest_id is not None else 1
            data = [new_id, self.name, tag, self.desc, self.price]

            try:
                cursor.execute('INSERT INTO Prices (id, product, tag, description, price) VALUES (?, ?, ?, ?, ?)', data)
                conn.commit()
            except Exception as e:
                await interaction.response.send_message(f'Произошла ошибка:\n{e}', ephemeral=True)
            else:
                await interaction.response.send_message(f'Цена на предмет {self.name} добавлена!', ephemeral = True)
        elif self.action == "edit":

            # Fetch the current values of the item
            cursor.execute('SELECT * FROM Prices WHERE id = ?', (self.id,))
            item_data = cursor.fetchone()

            if item_data:
                # Update the columns with new values
                updated_name = self.name
                updated_tag = tag
                updated_desc = self.desc
                updated_price = self.price

                update_query = '''
                    UPDATE Prices
                    SET product = ?,
                    tag = ?,
                    description = ?,
                    price = ?
                    WHERE id = ?
                    '''

                try:
                    cursor.execute(update_query, (updated_name, updated_tag, updated_desc, updated_price, self.id))
                    conn.commit()
                    await interaction.response.send_message(f'Цена на предмет {self.name} обновлена!', ephemeral=True)
                except Exception as e:
                    await interaction.response.send_message(f'Произошла ошибка при обновлении:\n{e}', ephemeral=True)
            else:
                await interaction.response.send_message(f'Предмет с ID {self.id} не найден.', ephemeral=True)
        else:
            print("неизвестное действие, прошу ПОДУМАТЬ БЛЯТЬ И ПИСАТЬ КОД НОРМАЛЬНО")

        conn.close()

class DeleteItem(discord.ui.Modal):
    def __init__(self):
        super().__init__(title= "Удаление предмета")
    number = discord.ui.TextInput(label='id предмета', placeholder='Номер предмета для удаления. Виден на сайте.', required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            item_id = int(self.number.value)
        except Exception:
            interaction.response.send_message("id должен быть числом!", ephemeral = True)
        else:
            await delete_by_id(interaction = interaction, id = item_id)

class ManageItem(discord.ui.Modal):
    def __init__(self, option):
        super().__init__(title='Добавление/изменение предмета')
        self.option = option

    product_number = discord.ui.TextInput(label='id предмета', placeholder='Если не меняете предмет - бесполезно', required=False)
    name = discord.ui.TextInput(label='Название предмета', placeholder='Буханка белого хлеба', required= True)
    description = discord.ui.TextInput(
        label='Описание предмета',
        style=discord.TextStyle.long,
        placeholder='Буханка белого хлеба весом около 500 грамм. Сделана из отборных сортов пшеницы.',
        required=False,
        max_length=500
    )
    price = discord.ui.TextInput(label = 'цена в ОТН', placeholder= '500', required= True)

    async def on_submit(self, interaction: discord.Interaction):

        try:
            item_id_num = int(self.product_number.value)
        except:
            item_id_num = -1
        try:
            money = int(self.price.value)
        except:
            await interaction.response.send_message('Цена была указана словами или графа имеет буквы. Цена не должна содержать букв или других символов', ephemeral=True)
        else:
            tag_select = TagView(product_number = item_id_num, product = self.name.value, desc= self.description.value, price= money, tag_name_list= tag_name_list, action = self.option)
            await interaction.response.edit_message(content = "Теперь выберите тег!", view = tag_select)




    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
            await interaction.response.edit_message(content = 'Что-то пошло не так! пинай калитиса!', view = None)
            traceback.print_exception(type(error), error, error.__traceback__)


class TagView(View):
    def __init__(self, product_number, product, desc, price, tag_name_list, action):
        self.product = product
        self.desc = desc
        self.price = price
        self.product_number = product_number
        self.tag_name_list = tag_name_list
        self.action = action
        super().__init__()
        self.add_item(TagChoose(id = self.product_number, name=self.product, desc=self.desc, price=self.price, tag_name_list=tag_name_list, action = self.action))


class InitView(View):
    def __init__(self):
        super().__init__()

    @button(label='Добавить предмет', custom_id='add')
    async def additem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ManageItem(button.custom_id))

    @button(label='Изменить предмет', custom_id='edit')
    async def edititem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ManageItem(button.custom_id))

    @button(label='Удалить предмет', custom_id='delete')
    async def delitem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DeleteItem())

async def get_price_info(id_to_retrieve):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    select_query = f"SELECT * FROM Prices WHERE id = {id_to_retrieve}"
    cursor.execute(select_query)
    row = cursor.fetchone()
    conn.close()

    return row
