// window.open('https://youtu.be/_u-JFPxBS2M', '40조', 'width = 500, height = 500, top = 100, left = 200, location = no');
jQuery( function() {
        jQuery( '#background' ).YTPlayer();
      } );
$(document).ready(function () {
    listing();
});

function listing() {
    $('#cards-box').empty()
    $.ajax({
        type: 'GET',
        url: '/musinsa',
        data: {},
        success: function (response) {
            let rows = response['musinsas']
            for (let i = 0; i < rows.length; i++) {
                let rank = rows[i]['rank']
                let comment = rows[i]['comment']
                let title = rows[i]['title']
                let image = rows[i]['image']
                let price = rows[i]['price']
                let sex = rows[i]['sex']
                let url = rows[i]['url']
                let num = rows[i]['num']
                let dune = rows[i]['dune']
                let temp_html = ``
                if (dune === 0) {
                    temp_html = `<tr>
                                        <th scope="row">${rank}위</th>
                                        <td><img src="${image}" onclick="location.href='/comment?rank=${rank}'" alt=""></td>
                                        <td><h4 onclick="location.href='${url}'">${title}</h4><p>${comment}</p><p>${price}</p>
                                        <button onclick="location.href='/reply/${comment}'" type="button" class="btn-1">후기</button>
                                        </td>
                                        <td>${sex}</td>
                                        <td onclick="event.cancelBubble=true">
                                            <button class="fa" onclick="done_musinsa(${num})"><span class="like"><i class="fa-regular fa-star"></i></span></button>
                                        </td>
                                    </tr>`

                } else {
                    temp_html = `<tr>
                                        <th scope="row">${rank}위</th>
                                        <td><img src="${image}" onclick="location.href='${url}'" alt=""></td>
                                        <td><h4 onclick="location.href='${url}'">${title}</h4><p>${comment}</p><p>${price}</p>
                                        <button onclick="location.href='/reply/${comment}'" type="button" class="btn-1">후기</button>
                                        </td>
                                        <td>${sex}</td>
                                        <td onclick="event.cancelBubble=true">
                                            <button class="fa" onclick="deleteStar(${num})"><span class="like"><i class="fa-solid fa-star"></i></span></button>
                                        </td>
                                    </tr>`
                }
                $('#cards-box').append(temp_html)
            }
        }
    })
}

$(document).ready(function () {
    let weatherIcon = {
        '01': 'fas fa-sun',
        '02': 'fas fa-clouds-sun',
        '03': 'fas fa-cloud',
        '04': 'fas fa-cloud-meatball',
        '09': 'fas fa-cloud-sun-rain',
        '10': 'fas fa-cloud-showers-heavy',
        '11': 'fas fa-poo-storm',
        '13': 'fas fa-snowflake',
        '50': 'fas fa-smog'
    };

    $.ajax({
        url: 'http://api.openweathermap.org/data/2.5/weather?q=Seoul&appid=bc93a7cbed56048a9a9214bd29ef4b25&units=metric',
        dataType: 'json',
        type: 'GET',
        success: function (data) {
            var $Icon = (data.weather[0].icon).substr(0, 2);
            var $Temp = Math.floor(data.main.temp) + '°';
            var $City = data.name;

            $('.CurrIcon').append('<i class="' + weatherIcon[$Icon] + '"></i>');
            $('.CurrTemp').prepend($Temp);
            // $('.City').append($City);
        }
    })
});


function done_musinsa(num) {
    $.ajax({
        type: "POST",
        url: "/musinsa/done",
        data: {num_give: num},
        success: function (response) {
            alert(response["msg"])
            window.location.reload()
        }
    });
}

function deleteStar(num) {
    $.ajax({
        type: 'POST',
        url: '/musinsa/delete',
        data: {'num_give': num},
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    });
}