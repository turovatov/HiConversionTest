<html>
<body>
    <%block name="text">
        <span>
            Вы получили инвайт с тестового задания от пользователя ${ name }.<br>
            Чтобы зарегистрироваться перейдите по
        </span>
        <span>
            <a href="${ href }">
                ссылке
            </a>
        </span>
    </%block>
</body>
</html>