$(function () {
    bindDeleteEvent()
})

function bindDeleteEvent() {
    $('.delete-btn').on('click', function () {
        $('#deleteModal').modal('show');
        DELETE_ID = $(this).attr('data-cid')
    })
    $("#btnCancelDelete").on('click', function () {
        console.log("取消了")
        $("#deleteModal").modal('hide');
    });
    $('#btnConfirmDelete').on('click', function () {
        console.log("提交了")
        $('#deleteModal').modal('hide');
        $.ajax({
            url: DELETE_URL,
            type: "GET",
            data: {cid: DELETE_ID},
            dataType: "JSON",
            success: function (res) {
                if (res.status) {
                    // 删除成功
                    // 方式一：页面的刷新
                    // location.reload();
                    // 方式二：找到当前数据行，删除
                    $("tr[data-row-id='" + DELETE_ID + "']").remove();
                    $("#deleteModal").modal('hide');
                } else {
                    // 删除失败
                    $("#deleteError").text(res.detail);
                }
            }
        })
    })
}