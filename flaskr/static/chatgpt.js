$(document).ready(function() {
    // textareaタグを全て取得
    $("textarea").each(function() {
        // // デフォルト値としてスタイル属性を付与
        // $(this).css("height", $(this).prop("scrollHeight"));
  
        // inputイベントが発生するたびに関数呼び出し
        $(this).on("input", function() {
            // textareaの高さを計算して指定
            $(this).css("height", "auto");
            $(this).css("height", $(this).prop("scrollHeight") + "px");
            var divHeight = parseInt($(this).prop("scrollHeight")) + 2;
            $('.bottom-fixed').css("height", divHeight + "px");
            $('.scrollable-content').css("bottom", divHeight + "px");
        });
    });

    $(".toggle").on("click", function() {
        $(this).toggleClass("checked");
        if(!$('input[name="audioOn"]').prop("checked")) {
            $(".toggle input").prop("checked", true);
            $('#audioCredit').show();
        } else {
            $(".toggle input").prop("checked", false);
            $('#audioCredit').hide();

            const audio = document.querySelector("audio");
            audio.pause();
        }
    });
    if ($('#audioToggle').prop('checked')) {
        $('#audioCredit').show();
    } else {
        $('#audioCredit').hide();
    }

    var charId = getCurrentDateTime();
    $('#chatid_input').val(charId);

    const recognition = new webkitSpeechRecognition();
    recognition.lang = "ja";
    recognition.continuous = true;
    recognition.onresult = (event) => {
        const results = event.results;
        console.log(results[0][0].transcript);
        $('#content_input').val(results[0][0].transcript);
        submitToServer();
    };
    $('#btn_voiceRec').mousedown(function() {
        recognition.start();
    });
    $('#btn_voiceRec').mouseup(function() {
        recognition.stop();
    });
});

function getCurrentDateTime() {
    var now = new Date();
    var year = now.getFullYear();
    var month = ("0" + (now.getMonth() + 1)).slice(-2); // Months are zero indexed, so we add 1
    var day = ("0" + now.getDate()).slice(-2);
    var hour = ("0" + now.getHours()).slice(-2);
    var minute = ("0" + now.getMinutes()).slice(-2);
    var second = ("0" + now.getSeconds()).slice(-2);
    var millisecond = ("00" + now.getMilliseconds()).slice(-3); // Milliseconds can be 1-3 digits long
    return "" + year + month + day + hour + minute + second + millisecond;
}

function appendContent(inputText, role) {
    // $('.contents_bottom_padding').remove();

    // var parentWidth = $('#contents_field').width();
    // var childMaxWidth = parentWidth * 0.66;
    var contentsField = $('#contents_field');

    var tmpInDiv = $('<span>').text(inputText);
    var saysDiv = $('<div>').html(tmpInDiv.text().replace(/\n/g, '<br>')).addClass('says');
    var inputDiv = $('<div>').append(saysDiv).addClass('message-block').addClass(role);
    contentsField.append(inputDiv);

    // スクロールする
//    var h = contentsField.height();
    var h = contentsField.prop('scrollHeight');
    contentsField.delay(100).animate({
//        scrollTop: $(document).height()
        scrollTop: h
    }, 1500);
}

function playAudio(path) {
    const audio = document.querySelector("audio");
    audio.src = path; // URL.createObjectURL(path);
    audio.play();
}

function submitToServer() {
    var inputText = $('#content_input').val().trim();
    var chatId = $('#chatid_input').val().trim();
    if (chatId === "") {
        var charId = getCurrentDateTime();
        $('#chatid_input').val(charId);
    }
    if (inputText === "") {
        $('#content_input').focus();
        return;
    }
    $('#content_input').val("");
    $('#content_input').focus();
    appendContent(inputText, 'user');

    console.log("#audioOn=" + $('#audioOn').prop('checked'));

    $.ajax({
        url: 'http://127.0.0.1:5505/chat',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ chatId: chatId, content: inputText, 
            audioOn: $('#audioOn').prop('checked'), speaker: $('#audioCredit').val() }),
        dataType: 'json',
        success: function(data) {
            // Assume that 'data' is an object and we want to extract 'content' from it
            var result = data.result;
            var role = data.role;
            var content = data.content;
            var audioPath = data.audio_path;
            appendContent(content, role);
            if (audioPath !== null) {
                playAudio('http://127.0.0.1:5505' + audioPath);
            }
            if (result !== true) {
                console.log("result is not true. data=" + JSON.stringify(data, null, 2));  // This will print the data as a nicely formatted JSON string
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error('Error', textStatus, errorThrown);
        }
    });
}

var keysPressed = {};
$('#content_input').keydown(function(event) {
    keysPressed[event.key] = true;

    if ((keysPressed['Control'] || keysPressed['Meta']) && keysPressed['Enter']) {
        submitToServer();
    }
});

$('#content_input').keyup(function(event) {
    delete keysPressed[event.key];
});

$('#btn_submit').click(function() {
    submitToServer();
});

$('#btn_newchat').click(function() {
    $('#chatid_input').val(getCurrentDateTime());
});

$('#btn_clearchat').click(function() {
    $('#chatid_input').val("");
});