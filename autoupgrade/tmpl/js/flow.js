function finish() {
    var options = [];
    for (var i = verList.length - 1; i >= 0; i--) {
        options[verList.length - i - 1] = { 'value': verList[i], 'label': verList[i] };
    }
    var server_list = [];
     for (var i = serverListOri.length - 1; i >= 0; i--) {
        server_list[serverListOri.length - i - 1] = { 'value': serverListOri[i], 'label': serverListOri[i] };
    }
    
    var appList = [];
    i = 0
     for (var val in appListOri) {
        var app = appListOri[val]
        appList[i] = { 'value': app.value, 'label': app.name };
        i++;
    }
    // 创建根实例
    new Vue({
        el: '#app-1',
        data: {
            form: {
                verOptions: options,
                versionNo:'',
                isSub:false,
                subBtnDisabled: false,
                updatePer: 5,
                curOper:"download",
                curStatus:"",
                verTypeOptions:[{"label":"test","value":"1"},{"label":"project","value":"2"}],
                verType:'',
                destServerOptions:server_list,
                destServer:'',
                app:'',
                appOptions:appList
            }
        },
        methods: {

            setProcessResult(data) {
                var result = JSON.parse(data)
                this.form.updatePer = result.process;
                if (this.form.updatePer >= 100) {
                    clearInterval(this.timer);
                    this.form.curOper = "finish";
                    this.form.curStatus = "success"
                    alert(result.msg);
                    this.form.subBtnDisabled = false;
                }
                else if (this.form.updatePer < 0) {
                    clearInterval(this.timer);
                    this.form.curOper = "exception";
                    this.form.curStatus = "exception"
                    alert(result.msg);
                    this.form.subBtnDisabled = false;
                }
            },
            
            getProcess(result) {
                curForm = this.form;
                that = this;
                var data = JSON.parse(result)
              
                if (data.result == 1) {
                this.timer = setInterval(function() {
                    $.get("getUpdatePer", {"destServer":curForm.destServer}, that.setProcessResult) 
                }, 5000);
                }
                else {
                    alert(data.msg)
                    this.form.subBtnDisabled = false;
                }
            },
            onSubmit() {
                curForm = this.form;
                that = this;
                this.$refs.form.validate(function(result) {
                    if (result) {
                        curForm.isSub = true;
                        curForm.subBtnDisabled = true;
                        param = {"versionNo":curForm.versionNo, "verType":curForm.verType, 
                        "destServer": curForm.destServer,"appNo":curForm.app};
                        $.post("updateFlow", param, that.getProcess);
                    }
                    
                });
                
            },
            changeVerType() {
                verType = this.form.verType;
                curForm = this.form;
                curForm.verOptions = [];
                curForm.versionNo = '';
                
                $.get("getVer", {"verType": curForm.verType, "appNo":curForm.app}, function(result) {
                    var data = JSON.parse(result)
                    var verList = data.verList;
                    var tmpOp = [];
                    for (var i = verList.length - 1; i >= 0; i--) {
                        tmpOp[verList.length - i - 1] = { 'value': verList[i], 'label': verList[i] };
                    }
                    curForm.verOptions = tmpOp;
                });

                // this.$http.post('/updateFlow', data.form)
                // .then(function (response) {
                //  console.log(response);
                // })
                // .catch(function (error) {
                //  console.log(error);
                // });
            },
            beforeDestroy() {
                clearInterval(this.timer);
                //clearTimeout(this.timer);
            }
        }
    })
}