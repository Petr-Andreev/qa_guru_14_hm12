import allure
from selene import browser, have
import resource


class PracticeFormPage:

    def open(self):
        with allure.step('Открываем окно регистрации'):
            browser.open("/automation-practice-form")

    def fill_first_name(self, value):
        with allure.step(f'Вводим имя со значением: {value}'):
            browser.element('#firstName').type(value)

    def fill_last_name(self, value):
        with allure.step(f'Вводим фамилию со значением: {value}'):
            browser.element('#lastName').type(value)

    def fill_user_number(self, value):
        with allure.step(f'Вводим номер телефона со значением: {value}'):
            browser.element('#userNumber').type(value)

    def fill_user_email(self, value):
        with allure.step(f'Вводим почту со значением: {value}'):
            browser.element('#userEmail').type(value)

    def fill_gender(self):
        with allure.step(f'Выбираем гендер'):
            browser.element('[for="gender-radio-1"]').click()

    @allure.step('Выбираем дату рождения:')
    def fill_birthday(self, year, month, day):
        with allure.step(f'Кликаем на календарь'):
            browser.element('#dateOfBirthInput').click()
        with allure.step(f'Выбираем значение для месяца: {month}'):
            browser.element('.react-datepicker__month-select').type(month)
        with allure.step(f'Выбираем значение для года: {year}'):
            browser.element('.react-datepicker__year-select').type(year)
        with allure.step(f'Выбираем значение для дня: {day}'):
            browser.element(
                f'.react-datepicker__day--0{day}:not(.react-datepicker__day--outside-month)'
            ).click()

    def fill_subjects(self, value):
        with allure.step(f'Выбираем тематику: {value}'):
            browser.element('#subjectsInput').type(value).press_enter()

    def fill_checkbox(self, value):
        with allure.step(f'Выбираем тематику хобби'):
            browser.all('.custom-checkbox').element_by(have.exact_text(value)).click()

    def fill_foto(self, file):
        with allure.step(f'Загружаем на страницу фото: {file}'):
            browser.element('#uploadPicture').set_value(resource.path(file))

    def fill_address(self, value):
        with allure.step(f'Прописываем адрес проживания: {value}'):
            browser.element('#currentAddress').type(value)

    def fill_state(self, state):
        with allure.step(f'Выбираем штат: {state}'):
            browser.element('#react-select-3-input').type(state).press_enter()

    def fill_city(self, city):
        with allure.step(f'Выбираем город: {city}'):
            browser.element('#react-select-4-input').type(city).press_enter()

    def submit(self):
        with allure.step(f'Нажимаем кнопку "Сохранить"'):
            browser.element('#submit').press_enter()

    def successful_authentication(self, text):
        with allure.step(f'Убеждаемся, что появилась надпись {text}'):
            browser.element('#example-modal-sizes-title-lg').should(
                have.text(
                    f'{text}'
                )
            )

    @allure.step('Сверяем введенные данные')
    def should_registered_user_data(self, fio, email,
                                    gender, phone, birthday, subjects,
                                    hobbies, photo, street,
                                    state_and_city):
        browser.element('.table').all('td').even.should(have.exact_texts(
            f'{fio}',
            f'{email}',
            f'{gender}',
            f'{phone}',
            f'{birthday}',
            f'{subjects}',
            f'{hobbies}',
            f'{photo}',
            f'{street}',
            f'{state_and_city}'
        ))
