package com.example.demo;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.CheckBox;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.control.RadioButton;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleGroup;

public class MovieController {

    @FXML private TextField txtTitle;
    @FXML private TextField txtGenre;
    @FXML private TextField txtYear;
    @FXML private TextField txtRating;
    @FXML private ComboBox<String> cmbCountry;
    @FXML private ToggleGroup tgFormat;
    @FXML private RadioButton rbCinema;
    @FXML private RadioButton rbOnline;
    @FXML private CheckBox chbIsFavorite;
    @FXML private Label lblResult;

    @FXML
    public void initialize() {
        // Наполнение ComboBox пятью странами (Самостоятельная часть)
        cmbCountry.getItems().addAll(
                "Казахстан",
                "США",
                "Великобритания",
                "Франция",
                "Япония"
        );
        cmbCountry.getSelectionModel().selectFirst();
    }

    // Обработчик кнопки «Сформировать»
    @FXML
    private void onCreateClick() {
        String title = txtTitle.getText().trim();
        String genre = txtGenre.getText().trim();
        String yearStr = txtYear.getText().trim();
        String ratingStr = txtRating.getText().trim();
        String country = cmbCountry.getValue();

        // 1. Проверка на пустые поля
        if (title.isBlank() || genre.isBlank() || yearStr.isBlank() || ratingStr.isBlank()) {
            showError("Пожалуйста, заполните все текстовые поля формы.");
            return;
        }

        // 2. Валидация года через try-catch (Перехват букв)
        int movieYear;
        try {
            movieYear = Integer.parseInt(yearStr);
        } catch (NumberFormatException e) {
            showError("Год выпуска должен содержать только цифры (буквы недопустимы)!");
            return;
        }

        // Логическая проверка диапазона года (кинематограф начался в 1895 году)
        if (movieYear < 1895 || movieYear > 2026) {
            showError("Введите корректный год выпуска фильма (от 1895 до 2026).");
            return;
        }

        // 3. Валидация рейтинга через try-catch (Перехват некорректного дробного формата)
        double movieRating;
        try {
            movieRating = Double.parseDouble(ratingStr);
        } catch (NumberFormatException e) {
            showError("Рейтинг должен быть числом (например, 8.5 или 9)!");
            return;
        }

        // Проверка диапазона рейтинга
        if (movieRating < 0.0 || movieRating > 10.0) {
            showError("Рейтинг фильма должен быть в пределах от 0.0 до 10.0.");
            return;
        }

        // Получение значений из RadioButton и CheckBox (Самостоятельная часть)
        RadioButton selectedFormat = (RadioButton) tgFormat.getSelectedToggle();
        String format = selectedFormat.getText();
        String favoriteStatus = chbIsFavorite.isSelected() ? "Да" : "Нет";

        // Формирование и вывод итоговой карточки
        lblResult.setText(
                "Название: " + title + "\n" +
                        "Жанр: " + genre + "\n" +
                        "Год выпуска: " + movieYear + " г.\n" +
                        "Рейтинг Кинопоиска: " + movieRating + " / 10\n" +
                        "Страна: " + country + "\n" +
                        "Формат просмотра: " + format + "\n" +
                        "В избранном: " + favoriteStatus
        );
    }

    // Обработчик кнопки «Очистить»
    @FXML
    private void onClearClick() {
        txtTitle.clear();
        txtGenre.clear();
        txtYear.clear();
        txtRating.clear();
        cmbCountry.getSelectionModel().selectFirst();
        rbCinema.setSelected(true);
        chbIsFavorite.setSelected(false);
        lblResult.setText("");
        txtTitle.requestFocus();
    }

    // Обработчик кнопки «Выход»
    @FXML
    private void onExitClick() {
        Platform.exit();
    }

    // Метод вывода сообщений об ошибках
    private void showError(String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle("Ошибка валидации");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
}