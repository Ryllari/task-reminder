import os
from datetime import datetime
from tasks import send_reminder

def main():
    running = True
    while running:
        os.system('clear')

        print("***************************************")
        print("************** LEMBRA AÍ! *************")
        print("***************************************")
        print("\n1 - Adicionar lembrete único")
        print("\n2 - Adicionar lembrete diário")
        print("\n3 - Adicionar lembrete hora em hora")
        print("\n4 - Adicionar lembrete minuto em minuto")
        print("0 - Sair e desabilitar lembretes")

        option = input("\nEscolha uma opção:")

        if option == '0':
            print("Até mais!")
            running = False
            break

        elif option == '1':
            create_unique_reminder()

        elif option == '2':
            create_periodic_reminder("daily")

        elif option == '3':
            create_periodic_reminder("hour")

        elif option == '4':
            create_periodic_reminder("minute")

        else:
            print("Opção inválida!")

        input("\nPressione qualquer tecla para voltar ao menu principal...")


def create_unique_reminder():
    reminder = input("O que você deseja lembrar? \n")
    dt_reminder = input(f"Quando devemos te lembrar de '{reminder}'? (Formato: dd/mm/aaaa HH:MM:SS) \n")
    try:
        reminder_date = datetime.strptime(dt_reminder, '%d/%m/%Y %H:%M:%S')
        dt_in_seconds = (reminder_date - datetime.now()).total_seconds()
        if dt_in_seconds < 0:
            print("Não foi possível agendar para o horário desejado...\nSó podemos te lembrar de compromissos futuros.")
            return
        send_reminder.s(reminder).apply_async(countdown=dt_in_seconds)
    except ValueError:
        print("Não foi possível agendar para o horário desejado...\nVerifique se o formato digitado é valido e tente novamente!")


def create_periodic_reminder(frequency):
    reminder = input("O que você deseja lembrar? \n")

    if frequency == "daily":
        with open("periodics/daily.txt", "a+") as f:
            f.write(f"{reminder}\n")
            f.close()
    elif frequency == "hour" :
        with open("periodics/hour.txt", "a+") as f:
            f.write(f"{reminder}\n")
            f.close()
    else:
        with open("periodics/minute.txt", "a+") as f:
            f.write(f"{reminder}\n")
            f.close()

    print(f"Lembrete '{reminder}' agendado!")
    

if __name__ == "__main__":
    os.system("celery -A tasks worker -B --detach")
    main()
    os.system("pkill -9 -f 'celery'")