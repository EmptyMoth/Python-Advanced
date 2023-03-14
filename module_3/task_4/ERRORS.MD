1. `__init__`
   > Исправленно начальное значение `address` с `""` на `None`.
2. `get_age`
   > Был добавлен модуль `import datetime`, поскольку его функционал использован в методе.\
   > Выдавало отрицательное значение.\
   > Исправленно `return self.yob - now.year` на `return now.year - self.yob`.
3. `set_name`
   > Не использовала передаваемое значение.\
   > Исправленно `self.name = self.name` на `self.name = name`.
4. `set_address`
   > Опечатка в присваивании переменой.\
   > Исправленно `self.address == address` на `self.address = address`.
5. `is_homeless`
   > Не использовалось значение переменой из самого класса.\
   > Исправленно `return address is None` на `return self.address is None`.
6. Общее
   > Была добавлена типизация для улучшения работы с кодом.