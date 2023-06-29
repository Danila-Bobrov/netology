<h1 tabindex="-1" dir="auto"><a id="user-content-дипломная-работа-vkinder" class="anchor" aria-hidden="true" href="#дипломная-работа-vkinder"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"></a>Дипломная работа 'VKinder'</h1>
<h2 tabindex="-1" dir="auto"><a id="user-content-запуск-программы" class="anchor" aria-hidden="true" href="#запуск-программы"></a>Запуск программы</h2>
<ol dir="auto">
<li>Установка необходимых библиотек:</li>
</ol>
<div class="snippet-clipboard-content notranslate position-relative overflow-auto"><pre class="notranslate"><code>    pip install vk_api
    pip install psycopg2
</code></pre><div class="zeroclipboard-container position-absolute right-0 top-0">
    <clipboard-copy aria-label="Copy" class="ClipboardButton btn js-clipboard-copy m-2 p-0 tooltipped-no-delay" data-copy-feedback="Copied!" data-tooltip-direction="w" value="    pip install vk_api
    pip install psycopg2" tabindex="0" role="button">
    </clipboard-copy>
  </div></div>
  <ol start="2" dir="auto">
<li>Заполнение переменных в файле config.py     <a href="https://vkhost.github.io/" rel="nofollow">Токен пользователя (acces_token) можно получить здесь</a></li>
<li>Запуск файла interface.py</li>
<li>Взаимодействие с ботом начинается введения любого сообщения в диалоге с сообществом, чей токен (community_token) указан в файле config.py</li>
</ol>
<h2 tabindex="-1" dir="auto"><a id="user-content-задание-к-дипломной-работе" class="anchor" aria-hidden="true" href="#задание-к-дипломной-работе"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"></a>Задание к дипломной работе</h2>
<p dir="auto">Необходимо разработать приложение для знакомств, эталоном которого является Tinder. Приложение предоставляет простой интерфейс для выбора понравившегося человека.</p>
<p dir="auto">Используя данные из VK, нужно сделать сервис намного лучше, чем Tinder, а именно: чат-бота 'VKinder'. Бот должен искать людей, подходящих под условия, на основании информации о пользователе из VK:</p>
<ul dir="auto">
<li>возраст</li>
<li>пол</li>
<li>город</li>
<li>семейное положение</li>
</ul>
<p dir="auto">У тех людей, которые подошли по требованиям пользователю, получать топ-3 популярных фотографии профиля и отправлять их пользователю в чат вместе со ссылкой на найденного человека.
Популярность определяется по количеству лайков.</p>
<h2 tabindex="-1" dir="auto"><a id="user-content-требование-к-сервису" class="anchor" aria-hidden="true" href="#требование-к-сервису"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"></a>Требование к сервису</h2>
<ol dir="auto">
<li>Код программы удовлетворяет PEP8;</li>
<li>Получать токен от пользователя с нужными правами;</li>
<li>Программа декомпозирована на функции/классы/модули/пакеты;</li>
<li>Результат программы записывать в БД (PostreSQL);</li>
<li>Люди не должны повторяться при повторном поиске;</li>
<li>Не запрещается использовать внешние библиотеки для vk.</li>
</ol>
