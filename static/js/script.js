function ActivateEditable(e) {
    e.editable({
        title: 'Введите отметку',
        url: '',
        value: {
            ts:"",
            desc: "ввести отметку"
        },
        validate: function (value) {
            if (value.ts == '') return 'ts is required!';
        },
        display: function (value) {
            if (!value) {
                $(this).empty();
                return;
            }
            var desc=$('<div>').text(value.desc).html()
            var ts=$('<div>').text(value.ts).html()
            if (desc == "ввести отметку") {
                var html = desc;
            }else{
                var html = '<b>' + ts + 'ч. ' + '</b> ' + desc;
            }
            $(this).html(html);
        }
    });
}



function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function initialise() {
    $('.tree').treegrid();
    $('.edit-timestamp').each(function (index) {
        ActivateEditable($(this))
    });


};


$(document).ready(function () {
    initialise()
    $.fn.editable.defaults.mode = 'popup';
    // текущая дата активная
    var todaysDate = new Date();
    function convertDate(date) {
        var yyyy = date.getFullYear().toString();
        var mm = (date.getMonth() + 1).toString();
        var dd = date.getDate().toString();
        var mmChars = mm.split('');
        var ddChars = dd.split('');
        return yyyy + '-' + (mmChars[1] ? mm : "0" + mmChars[0]) + '-' + (ddChars[1] ? dd : "0" + ddChars[0]);
    }
    today=convertDate(todaysDate);
    $('[data-date="' + today + '"]').addClass('date-selectdate');

    // Отправить отметку
    $(document).on('submit','.form-inline',function(e){
        e.preventDefault();
        var task_id = $(this).data('task_id')
        var task_type = $(this).data('task_type')
        var focus_date= $('#focus_date').data('focus_date')
        var data = {};
        data.ts=$(this).find('.ts-input').val()
        data.desc=$(this).find('.desc-input').val()
        var csrftoken = getCookie('csrftoken');
        console.log(csrftoken )
        // data["csrfmiddlewaretoken"] = $(this).find('[name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrftoken

        data.focus_date = focus_date
        data.task_id = task_id
        data.task_type = task_type
        $.ajax({
            url: '/SendTimestamp/',
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                 var data = {};
                 data.date = focus_date;
                 console.log(focus_date);
                 $.ajax({
                    url: '/async_update_panels/',
                    data: data,
                    type: 'GET',
                    success: function (data) {
                        $('#panels').html(data);
                        initialise()
                    }
                 });
            },
            error: function () {
                console.log('error');
            }
        })
    })
    // Поменять день
    $(document).on('click', '.date-cell', function (e) {
        e.preventDefault();
        var data = {};
        data.date = $(this).data("date")
        // Рисуем задачи для этой даты b
        $.ajax({
            url: '/async_update_panels/',
            data: data,
            type: 'GET',
            success: function (data) {
                $('#panels').html(data);
                initialise()
            }
        });
        // Делаем выбранную дату активной
        $('.date-selectdate').removeClass('date-selectdate')
        $(this).addClass('date-selectdate')
    })
    // Смена месяца
    $(document).on('click', '.glyphicon-menu-left, .glyphicon-menu-right', function (e) {
        e.preventDefault();
        //
        var data = {};
        data.nav = $(this).data("nav")
        data.month = $(this).data("month")
        data.year = $(this).data("year")
        // Рисуем задачи для этой даты b
        $.ajax({
            url: '/async_update_navbar/',
            data: data,
            type: 'GET',
            success: function (data) {
                $('.ts-header').replaceWith(data);
            }
        })
    });
    // При клике на задачу добавить поля для отправки отметки
    $(document).on('click', '.task', function (e) {
        e.preventDefault();
        task_id=$(this).attr('id')
        
        $("tr.for-new-edit#"+task_id).removeClass('hidden').addClass('treegrid treegrid-parent-'+task_id).find('.ts-input').focus()


        $('.tree').treegrid();
    });



})




