//varは、JavaScriptプログラムで利用する変数を宣言するための命令の１つ、　var 変数名 = 値
//jQueryで書いていく

//押されたボタンのDOMからcontent_idを取得して、JSON形式で/goodにPOST
$(function(){
    //以下はセレクタの中身を新規に作るという意味
    var $good = $('.good-btn'),
                contentId;
    //clickイベントを使い、$goodがクリックされた時に処理が実行されるようにイベントを設定
    $good.on('click',function(e){
        //stopPropagation: 要素のクリックなどで発生したイベントの伝播を阻止
        e.stopPropagation();
        //this: データ取得専用の変数
        var $this = $(this);
        //stringify:  JavaScript のオブジェクトや値を JSON 文字列に変換する　↓HTML側から受け取ったcontent_id
        var data = JSON.stringify({"content_id":$this.data('content_id')});
        $.ajax({
            type: 'POST',
            //url: Ajaxリクエストを送信するURLを指定
            url: '/good',
            data: data,
            //jsonフォーマットでデータが送信
            contentType:'application/json'
        //done: ajaxメソッドが成功した場合の処理
        }).done(function(data){
            $this.next().text(data);
            //toggleClassメソッド: 指定したクラス名の CSS がある場合は削除を行い、なければ追加する、色を赤→白また白→赤へ変更する
            $this.toggleClass('good-btn-active');
        //fail: ajaxメソッドが失敗した場合の処理
        }).fail(function(msg) {
            console.log('Ajax Error');
        });
    });
});
