# Project cli-tool:

<details><summary>Test task:</summary>

У нас есть публичный REST API для нашей базы данных:
https://rdb.altlinux.org/api/
У него есть метод
/export/branch_binary_packages/{branch}
в качестве бранча можно использовать sisyphus и p10
Нужно сделать модуль python и cli утилиту linux (использующую этот модуль на python), которая:
1) получает списки бинарных пакетов ветки sisyphus и p10
2) делает сравнение полученных списков пакетов и выводит JSON (структуру нужно придумать), в котором будет отображено:
- все пакеты, которые есть в p10 но нет в sisyphus
- все пакеты, которые есть в sisyphus но их нет в p10
- все пакеты, version-release которых больше в sisyphus чем в p10
Это нужно сделать для каждой из поддерживаемых веткой архитектур (поле arch в ответе).
Процесс разработки нужно оформить в виде git репозитория с историей всех изменений с самого первого этапа (без переписывания коммитов) и выложить, например, на github
Утилита должна запускаться под операционной системой Linux (проверяться будет на ALT Linux, версии 10), к ней должно быть README на английском языке, содержащее инструкцию по запуску.
Сравнение version-release согласно правилам версионирования rpm пакетов.

</details>

---

## Table of contents:

- [Installation and start](#installation-and-start)
- [Deletion](#deletion)
- [Author](#author)

---

## Installation and start

1.**Making the file executable**
```bash
chmod +x setup_cli_tool.sh
```

2.**Start-up**
```bash
./setup_cli_tool.sh
```

3.**Available commands in the console**

```bash
cli-tool --help
```
**Complete the test task**
```bash
cli-tool perform_task
```
[⬆ Table of contents](#table-of-contents)

---

## Deletion

**Go to the path - /usr/local/bin and delete the file**
```bash
sudo rm cli-tool
```
[⬆ Table of contents](#table-of-contents)

---

## Author
[I'am](https://github.com/Ell6969)

[⬆️At the beginning](#Project-cli-tool)
