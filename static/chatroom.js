$(function() {
    var conn = null;

    function log(msg) {
        var control = $('#log');
        control.html(control.html() + msg + '<br/>');
        control.scrollTop(control.scrollTop() + 1000);
    }

    function connect() {
        disconnect();
        conn = new SockJS('http://' + window.location.host + '/socket');
        log('Connecting...');
        conn.onopen = function(){
            log('Connected.');
            update_ui();
        };

        conn.onmessage = function(e) {
            var obj = eval("("+ e.data+")");
            if(obj.type=="1"){
                var user="<div id='"+obj.id+"'>"+obj.user+"</div>";
                $("#user").append(user);
            }
            else if(obj.type=="2"){
                $("#"+obj.id).remove();
            }
            var value="<span class='time_font'>"+obj.time+"<br/></span>"+obj.user+":"+obj.message;
            log(value);
        };

        conn.onclose = function() {
            log('Disconnected.');
            conn = null;
            update_ui();
        };
    }

    function disconnect() {
        if (conn != null) {
            log('Disconnecting...');

            conn.close();
            conn = null;

            update_ui();
        }
    }

    connect();

    $('form').submit(function() {
        var text = $('#text').val();
        conn.send(text);
        $('#text').val('').focus();
        return false;
    });
});