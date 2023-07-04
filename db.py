import sqlite3
import tg

conn = sqlite3.connect('carbase.db')
cursor = conn.cursor()


def check_db(new_cars):
    for car in new_cars:
        car_Id = car['Id']
        cursor.execute('SELECT Id FROM Cars WHERE Id = ?', (car_Id,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO Cars (id, title, link, price, location, mileage, img) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (car_Id, car['title'], car['link'], car['price'], car['location'], car['mileage'], car['img']))
            conn.commit()
            tg.send_notification(car)
        else:
            cursor.execute("SELECT id, price FROM cars WHERE Id = ?", (car['Id'],))
            old_price = cursor.fetchone()
            if old_price[1] != car['price']:
                cursor.execute("UPDATE cars SET price = ? WHERE id = ?", (car['price'], car_Id))
                conn.commit()
                tg.send_price_change_notification(car['title'], car['price'], car['link'])
    conn.commit()


def is_available(new_cars):
    cursor.execute('SELECT Id, title, link FROM Cars')
    all_cars = cursor.fetchall()

    for car_old_id, title, link in all_cars:
        if int(car_old_id) not in [int(car['Id']) for car in new_cars]:
            cursor.execute("DELETE FROM Cars WHERE Id = ?", (car_old_id,))
            tg.send_car_sold_notification(car_old_id, title, link)

    conn.commit()

