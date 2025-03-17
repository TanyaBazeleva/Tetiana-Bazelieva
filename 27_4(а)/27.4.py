import cgi
import cgitb
cgitb.enable()
def count(sequence):
    nums = list(map(int, sequence.split(',')))
    sign_changes = 0
    for i in range(len(nums) - 1):
        if nums[i] * nums[i + 1] < 0:
            sign_changes += 1
    return sign_changes

def main():
    print("Content-type: text/html\n")
    form = cgi.FieldStorage()
    sequence = form.getfirst("sequence", "").strip()

    if sequence:
        try:
            result = count(sequence)
            print(f"<h1>Результат: Кількість змін знаку - {result}</h1>")
        except ValueError:
            print("<h1>Помилка: Будь ласка, введіть коректну послідовність цілих чисел через кому.</h1>")
    else:
        print("<h1>Помилка: Поле введення не може бути порожнім.</h1>")

if __name__ == "__main__":
    main()
