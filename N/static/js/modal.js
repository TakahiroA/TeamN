// メンバー追加モーダル管理
$(function () {

    //追加ボタンを押した際
    $('#AMB').click(function () {
        //背景を付ける
        $("body").append('<div class="modal-bg"></div>');

        //モーダルウィンドウを表示
        $("#modal-bg,#modal-member").fadeIn("fast");

        //画面の背景もしくは戻るボタンを押したらモーダルを閉じる
        $('#modal-bg, #AMCB').click(function () {
            $("#modal-bg,#modal-member").fadeOut("fast", function () {
                $('#modal-bg').remove();
            });
        });
    });
});