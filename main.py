import os
import time
import glob
import logging

from config import DELAY, MAIN_URL, DOWNLOAD_FOLDER

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait as WW
from selenium.webdriver.support import expected_conditions as EC


def parse_xlsx(df: pd.DataFrame, driver: webdriver):
    '''
    Inputs:
        df - датафрейм со всеми сроками из загруженного excel
        driver - экземпляр драйвера chrome
    '''
    # Итерируемся по каждой строке датафрейма
    for i, row in df.iterrows():
        logging.info(f'Обрабатываю строку: \n{row.to_string()}')
        # Итерируемся по каждому столбцу в строке
        for column in df.columns:
            # Формируем label для поиска поля ввода, вулючая 2 исключения
            column_label = 'label' + ''.join([word for word in column.split(' ') if word != ' '])
            if column_label == 'labelPhoneNumber': column_label = 'labelPhone'
            if column_label == 'labelRoleinCompany': column_label = 'labelRole'

            # Находим инпут и вводим значение
            lableInput = WW(driver,DELAY).until(EC.presence_of_element_located((By.XPATH, f"//input[@ng-reflect-name='{column_label}']")))
            lableInput.send_keys(row[column])

            # Получаем новое значение инпута и проверяем, что значение ввелось правильно
            check_value = lableInput.get_attribute('value')
            if check_value != str(row[column]):
                error_str = f'Ошибка ввода значения в поле: {column_label}. Было введено "{check_value}" вместо "{row[column]}"'
                logging.error(error_str)
                raise Exception(error_str)
            
            logging.info(f'Успешно ввел значение в поле: {column_label}')

        # Прожимаем подтверждение
        WW(driver,DELAY).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Submit']"))).click()
    

def main():
    # Создаем папку для выгрузки excel
    if not os.path.exists(DOWNLOAD_FOLDER):
        logging.info('Создаю папку для выгрузки')
        os.mkdir(DOWNLOAD_FOLDER)

    # Указываем путь сохранения для excel
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : os.path.abspath(DOWNLOAD_FOLDER)}
    options.add_experimental_option("prefs", prefs)

    # Создаем экземпляр драйвера и прогружаем актуальный драйвер хрома
    logging.info('Запускаю хром и перехожу по ссылке')
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url=MAIN_URL)

    # Скачиваю файл и считываю его в датафрейм
    WW(driver,DELAY).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),' Download Excel ')]"))).click()
    time.sleep(5)
    path_for_serach = os.path.join(os.path.abspath(DOWNLOAD_FOLDER), '*.xlsx')
    latest_file = max(glob.glob(path_for_serach), key=os.path.getctime)

    # Проверяем загрузился ли файл
    if not latest_file:
        raise Exception('Не найден файл после загрузки')
    
    logging.info(f'Скачал файл и сохранил по пути: {latest_file}')
    df_input = pd.read_excel(latest_file)

    # Прожимаем старт
    logging.info('Прожимаю старт')
    WW(driver,DELAY).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Start')]"))).click()

    # Начинаю внесение строк
    parse_xlsx(df=df_input, driver=driver)

    # Делаем и сохраняем скрин скрин
    driver.get_screenshot_as_file('result.png')
    logging.info('Сделал и сохранил скриншот')


if __name__ == "__main__":
    try:
        # Инициализирую логгер
        logging.basicConfig(
            level=logging.INFO, 
            filename='log.log', 
            filemode='w',
            format="%(asctime)s %(levelname)s %(message)s")
        # Запускаем основную функцию
        logging.info('Начало работы')
        main()
    except Exception as e:
        logging.error(f'Ошибка выполнения скрипта: {e}')
