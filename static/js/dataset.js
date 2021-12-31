function name_dataset_js() {
    var name = prompt("请输入您的数据集名称", "");
    var tag = prompt("请输入一个数据集标签（如果无，直接点击OK）", "")
        if (name!="" && name != null) {
            $.ajax({
                    url : "/name_dataset",
                    data :{'name' : name,
                            'tag': tag},
                    type : "POST",
                    success : function(data){
                                if (data =="200"){
                                    alert("命名成功");
                                    window.location.replace('/');
                                }
                                else{
                                    alert("对不起，您没有该权限");
                                }
                          }
                })
        }
}

function delete_dataset_js() {
    if (confirm('您是否要删除当前仍未发布的数据集?')) {
      $.ajax({
                url : "/delete_dataset",
                type : "POST",
                success : function(data){
                            if (data =="200"){
                                alert('删除成功，返回首页。');
                                window.location.replace('/');
                            }
                            else{
                                alert("删除失败！");
                            }
                      }
            })
    }
}