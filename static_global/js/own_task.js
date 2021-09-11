// variable that keeps all the filter information

var send_data = {}


$(document).ready(function () {
    send_data['choice'] = [];

    // reset all parameters on page load

    resetFilters();
    // bring all the data without any filters

    getAPIData();

    getFacultyen();

    getGraden();

    getTopice();

    $('#topics').change(function () {
        send_data['topic'] = this.value;
        getAPIData();
    })

    $('#grades').change(function () {
        $('#topics').val("all");

        send_data['topic'] = '';


        if (this.value == 'all') {
            send_data['grade'] = '';
        } else {
            send_data['grade'] = this.value;
        }

        getTopice(faculty = $('#faculties').val(), grade = this.value);

        getAPIData();
    })

    $('#faculties').change(function () {
        $('#topics').val("all");
        $('#grades').val("all");
        send_data['topic'] = '';
        send_data['grade'] = '';

        if (this.value == 'all') {
            send_data['faculty'] = '';
        } else {
            send_data['faculty'] = this.value;
        }

        getTopice(faculty = this.value, grade = null)
        getGraden(faculty = this.value);

        getAPIData();
    })

    // on selecting the keyword option



    $('#keywords').keyup(function () {
        if (this.value == "") {
            send_data['keywords'] = "";
        } else {
            send_data['keywords'] = this.value;
        }
        getAPIData();
    });

    // display the results after reseting the filters

    $("#display_all").click(function () {
        resetFilters();
        getAPIData();
    })



})

function toggleSendData(e) {
    if (e.checked) {
        send_data['choice'].push(e.id);
    } else {
        const index = send_data['choice'].indexOf(e.id);
        if (index !== -1) {
            send_data['choice'].splice(index, 1);
        }
    }
}

function resetFilters() {
    $("#keywords").val("");


    send_data['keywords'] = '';
    send_data['topic'] = '';
    send_data['grade'] = '';
    send_data['faculty'] = '';

    send_data['format'] = 'json';

    getFacultyen();
    getGraden();
    getTopice();

}

/**.
    Utility function to showcase the api data 
    we got from backend to the table content
**/
function putTableData(result) {
    // saveCheckedInputs();
    console.log(result);

    // creating table row for each result and

    // pushing to the html cntent of table body of listing table

    let row;

    if (result['results'].length > 0) {
        $("#no_results").hide();
        $("#list_data").show();
        $("#listing").html("");
        $.each(result['results'], function (a, b) {
            row = "<tr><td class='px-5 align-middle'><input onChange='toggleSendData(this)'" + "class='form-checkbox' name='" + b.id + "' id='" + b.id + "' type='checkbox'>"
                + "</td><td class='align-middle'><button id='button_" + b.id + "' class='btn' onclick='togglePreview(this)'> <i class='far fa-eye'></i>"
                + "</button><a class='text-reset text-decoration-none' href = '/Task/Bearbeiten/" + b.id + "'> <i class='fas fa-pen'></i> </a></td>"
                + "<td class='align-middle'><a   > " + b.headline + "</a></td > " +
                "<td class='align-middle'>" + b.description +
                "<td class='align-middle'>" + b.created_by.last_name +
                "<td class='align-middle'>" + b.edited_by.last_name
                + "</td></tr>"
                + "<tr class='invisible' style='line-height: 0px'><td  class=''  colspan='6' id='preview_" + b.id + "'>"
                + "</td></tr>"
            $("#listing").append(row);
        });

        let choices = send_data['choice'];
        for (let i = 0; i < choices.length; i++) {
            $("#" + choices[i]).prop('checked', true);
        }
    }
    else {
        // if no result found for the given filter, then display no result

        $("#no_results h5").html("Keine Ergebnisse gefunden");
        $("#list_data").hide();
        $("#no_results").show();
    }


    // setting previous and next page url for the given result

    let prev_url = result["previous"];
    let next_url = result["next"];
    // disabling-enabling button depending on existence of next/prev page. 

    if (prev_url === null) {
        $("#previous").parent('li').addClass("disabled");
        $("#previous").prop('disabled', true);
    } else {
        $("#previous").parent('li').removeClass("disabled");
        $("#previous").prop('disabled', false);
    }
    if (next_url === null) {
        $("#next").parent('li').addClass("disabled");
        $("#next").prop('disabled', true);
    } else {
        $("#next").parent('li').removeClass("disabled");
        $("#next").prop('disabled', false);
    }
    // setting the url

    $("#previous").attr("url", result["previous"]);
    $("#next").attr("url", result["next"]);
    // displaying result count

    text_result_count = ""
    if (result['count'] === 1) {
        text_result_count += "Ergebnis"
    } else {
        text_result_count += "Ergebnisse"
    }

    $("#result-count span").html(result.count + " " + text_result_count);
}

$("#next").click(function () {
    // load the next page data and 

    // put the result to the table body

    // by making ajax call to next available url

    let url = $(this).attr("url");
    // let url = $('#list_data').attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (result) {
            putTableData(result);
        },
        error: function (response) {
            console.log(response)
        }
    });
})

$("#previous").click(function () {
    // load the previous page data and 

    // put the result to the table body 

    // by making ajax call to previous available url

    let url = $(this).attr("url");
    if (!url) {
        $(this).prop('all', true);
    }

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (result) {
            putTableData(result);
        },
        error: function (response) {
            console.log(response)
        }
    });
})

function getAPIData() {
    let url = $('#list_data').attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: send_data,
        beforeSend: function () {
            $("#no_results h5").html("Late Daten...");
        },
        success: function (result) {
            putTableData(result);
        },
        error: function (response) {

            $("#no_results h5").html("Etwas ist schiefelaufen");
            $("#list_data").hide();
        }
    });
}

function getUserData() {
    ajax('/api/user_listing')
        .then(function (result) {
            return result;
        })
        .catch(function () {
            console.log("error");
        })
}

function ajax(url) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.onload = function () {
            resolve(this.responseText);
        };
        xhr.onerror = reject;
        xhr.open('GET', url);
        xhr.send();
    });
}

$("#erstellen").click(function (e) {
    choices = send_data['choice']
    let url = $(this).data('href') + "?";
    for (let i = 0; i < choices.length; i++) {
        url += "aid=" + choices[i] + "&"
    }
    location.assign(url);
})

function togglePreview(element) {
    id = element.id.split('_')[1];
    let iFrameDiv = document.getElementById('preview_' + id);
    let iFrameDivParent = iFrameDiv.parentElement;


    if (iFrameDiv.firstChild) {
        let iFrame = iFrameDiv.firstChild;
        if (iFrame.classList.contains('invisible')) {
            iFrame.classList.remove('invisible');
            iFrame.setAttribute('height', '500px');
            iFrameDiv.setAttribute('height', '500px');
            iFrameDivParent.style.line_height = ('500px');
            iFrameDivParent.classList.remove('invisible');
        } else {
            iFrame.classList.add('invisible');
            iFrame.setAttribute('height', '0px');
            iFrameDiv.setAttribute('height', '0px');
            iFrameDivParent.style.line_height = ('0px');
            iFrameDivParent.classList.add('invisible');
        }
    } else {
        let iFrame = document.createElement('iframe');
        iFrameDiv.appendChild(iFrame);
        iFrame.setAttribute('src', '/media/pdf/' + id + '#view=FitH');
        iFrame.setAttribute('width', '100%');
        iFrame.setAttribute('height', '500px');
        iFrameDivParent.classList.remove('invisible');
        iFrameDivParent.height = '0px';
    }



}

function getFacultyen() {
    let url = $('#faculties').attr('url');

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            faculties_option = '<option value="all" selected>Alle</option>';
            $.each(result, function (a, b) {
                faculties_option += '<option value=' + b.id + '>' + b.name + '</option>'
            });
            $("#faculties").html(faculties_option)
        }
    })
}

function getGraden(faculty = null) {
    let url = $('#grades').attr('url');
    let data;
    if (faculty === null) {
        data = {}
    } else {
        data = { 'faculty': faculty }
    }

    $.ajax({
        method: 'GET',
        url: url,
        data: data,
        success: function (result) {
            grades_option = '<option value="all" selected>Alle</option>';
            $.each(result, function (a, b) {
                grades_option += '<option value=' + b.id + '>' + b.name + '</option>'
            });
            $("#grades").html(grades_option)
            getTopice(faculty = faculty, grade = null)
        }
    })
}


function getTopice(faculty = null, grade = null) {
    let url = $('#topics').attr('url');
    let data = { 'faculty': "", 'grade': "" };
    if (faculty !== null) {
        data.faculty = faculty
    }
    if (grade !== null) {
        data.grade = grade
    }
    $.ajax({
        method: 'GET',
        url: url,
        data: data,
        success: function (result) {
            topics_option = '<option value="all" selected>Alle</option>';
            $.each(result, function (a, b) {
                topics_option += '<option value=' + b.id + '>' + b.faculty.short_name + b.grade.name + ": " + b.description + '</option>'
            });
            $("#topics").html(topics_option);
        }
    })
};