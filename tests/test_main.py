import main
from data_formats import empty_db


def test_main_loads_data_dispatches_menu_and_exits(monkeypatch, capsys):
    db = empty_db()
    loaded_dirs = []
    selected_menus = []
    prompts = []
    inputs = iter(["invalid", "1", "2", "3", "4", "5", "6", "7", "0"])

    monkeypatch.setattr(main.save_load, "load_data",
                        lambda directory: loaded_dirs.append(directory) or db)
    for choice, name in (
        ("1", "course"),
        ("2", "student"),
        ("3", "classroom"),
        ("4", "activity"),
        ("5", "enrollment"),
        ("6", "timetable"),
        ("7", "sign_up"),
    ):
        monkeypatch.setattr(
            main,
            {
                "course": "course_menu",
                "student": "student_menu",
                "classroom": "classroom_menu",
                "activity": "activity_menu",
                "enrollment": "enrollment_menu",
                "timetable": "timetable_menu",
                "sign_up": "sign_up_menu",
            }[name],
            lambda selected_db, menu=name: selected_menus.append((menu, selected_db)),
        )
    def fake_input(prompt):
        prompts.append(prompt)
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    main.main()

    assert loaded_dirs == [main.DATA_DIR]
    assert selected_menus == [
        ("course", db),
        ("student", db),
        ("classroom", db),
        ("activity", db),
        ("enrollment", db),
        ("timetable", db),
        ("sign_up", db),
    ]
    assert len(prompts) == 9
    capsys.readouterr()


def test_main_routes_student_lookup_and_reports_missing_student(monkeypatch, capsys):
    monkeypatch.setattr(main.save_load, "load_data", lambda _: empty_db())
    inputs = iter(["2", "4", "S404", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    main.main()

    assert "找不到學生" in capsys.readouterr().out


def test_report_saves_only_successful_changes(monkeypatch, capsys):
    db = empty_db()
    saved = []
    monkeypatch.setattr(main.save_load, "save_data",
                        lambda saved_db, directory: saved.append((saved_db, directory)))

    main.report(db, ["資料錯誤"])
    main.report(db, [])
    main.report(db, main.NOT_DONE)

    output = capsys.readouterr().out
    assert "錯誤：資料錯誤" in output
    assert "完成，已存檔" in output
    assert saved == [(db, main.DATA_DIR)]


def test_activity_lookup_reports_missing_activity(monkeypatch, capsys):
    inputs = iter(["4", "A404"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    db = empty_db()

    main.activity_menu(db)

    assert "找不到活動" in capsys.readouterr().out


def test_input_converters():
    assert main.to_int("12") == 12
    assert main.to_int("abc") == "abc"
    assert main.to_schedule("1:3,4 2:b 1:5") == {
        "1": [3, 4, 5],
        "2": [11],
    }
