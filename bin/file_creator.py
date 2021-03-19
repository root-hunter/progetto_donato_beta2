import datetime
import time

import xlsxwriter

import bin.users as u
import bin.users_disponibility as ud
import telegram

bot_token = "1750316913:AAGXSDe61TrwdT3Qd_r6xAS3MLe7tx-YlpM"
genbot = telegram.bot.Bot(bot_token)

def create_export_users_excel(user_id):

    file_path = "./documents/excel_user_export/statistiche_dipendenti_"+str(datetime.datetime.now()).replace(' ', '_').replace('.', '_').replace(':', '_').replace('-', '_')+'.xlsx'
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    bold.set_align('center')
    bold.set_border(style=2)

    # Add a number format for cells with money.
    cell = workbook.add_format()
    cell_yes = workbook.add_format()
    cell_no = workbook.add_format()
    cell_date =  workbook.add_format()

    cell.set_align("center")
    cell.set_border(style=2)

    cell_yes.set_align("center")
    cell_yes.set_bg_color("green")
    cell_yes.set_border(style=2)

    cell_no.set_align("center")
    cell_no.set_bg_color("red")
    cell_no.set_border(style=2)

    cell_date.set_align("center")
    cell_date.set_border(style=2)
    cell_date.set_num_format("yyyy-mm-dd")


    # Write some data headers.
    worksheet.set_column(0, 0, 12)
    worksheet.set_column(1, 2, 20)
    worksheet.set_column(3, 4, 22)
    worksheet.set_column(5, 5, 15)
    worksheet.set_column(6, 6, 30)


    worksheet.set_column(0,7, 30)
    worksheet.write('A1', 'TELEGRAM ID', bold)
    worksheet.write('B1', 'NOME', bold)
    worksheet.write('C1', 'COGNOME', bold)
    worksheet.write('D1', "REGIONE", bold)
    worksheet.write('E1', 'PROVINCIA', bold)
    worksheet.write('F1', "DISPONIBILITA'", bold)
    worksheet.write('G1', 'AGGIORNAMENTO STATO', bold)


    expenses = u.get_users()


    # Start from the first cell below the headers.
    row = 1
    col = 0

    # Iterate over the data and write it out row by row.
    yellow_cell = workbook.add_format()

    yellow_cell.set_bg_color("yellow")
    yellow_cell.set_num_format_index(10)

    red_cell = workbook.add_format()
    red_cell.set_bg_color("red")
    print(expenses)
    n = 7
    for x in range(len(expenses)):
        print(expenses[x][6])
        if expenses[x][2] != None and expenses[x][3] != None:
            worksheet.write(row, 0, expenses[x][1], cell)
            worksheet.write(row, 1, expenses[x][2], cell)
            worksheet.write(row, 2, expenses[x][3], cell)
            worksheet.write(row, 3, str(expenses[x][7]), cell)
            worksheet.write(row, 4, expenses[x][8], cell)
            if expenses[x][4] == 1:
                worksheet.write(row, 5, "SI", cell_yes)
            elif expenses[x][4] == 0:
                worksheet.write(row, 5, "NO", cell_no)


            worksheet.write(row, 6, str(expenses[x][9]), cell_date)

            row += 1


    yellow_cell_result = workbook.add_format()
    yellow_cell_result.set_bg_color("yellow")
    yellow_cell_result.set_num_format_index(10)
    yellow_cell_result.set_border(2)

    for x in range(n):
        if x != n-2:
            worksheet.write(row, x, "", yellow_cell)
        elif x == n-3:
            worksheet.write(row, x, str("NUMERO DI DIPENDENTI ATTIVI"), yellow_cell)
        else:
            worksheet.write(row, x, round(ud.get_percent_active(),3), yellow_cell_result)

    worksheet.write(row, 0, "PERCENTUALE DIPENDENTI DISPONIBILI", yellow_cell)
    row += 1

    for x in range(n):
        if x != n-2:
            worksheet.write(row, x, "", yellow_cell)
        else:
            worksheet.write(row, x, round(ud.get_percent_inactive(),3), yellow_cell_result)

    worksheet.write(row, 0, "PERCENTUALE DIPENDENTI NON DISPONIBILI", yellow_cell)

    chart = workbook.add_chart({'type': 'pie'})

    chart.add_series({
        'name': 'SITUAZIONE ATTUALE',
        'categories': '=Sheet1!$A$'+str(row)+':$B$'+str(row+1),
        'values':     '=Sheet1!$F$9:$F$10',
        'points': [
        {'fill': {'color': '#5ABA10'}},
        {'fill': {'color': '#FE110E'}},
        {'fill': {'color': '#CA5C05'}},
    ]})
    worksheet.insert_chart('A'+str(row+2), chart)

    workbook.close()
    genbot.send_document(user_id, document=open(file_path, 'rb'))