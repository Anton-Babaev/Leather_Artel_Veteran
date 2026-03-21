// Основной JavaScript файл для сайта

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всех Bootstrap тултипов
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Функция для обновления количества товара в корзине (будет доработано)
    function updateCartCount() {
        // Здесь будет AJAX запрос для обновления счетчика корзины
        console.log('Корзина обновлена');
    }
    
    // Обработчик для добавления в корзину
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            // Здесь будет логика добавления в корзину
            alert('Товар добавлен в корзину!');
        });
    });
});