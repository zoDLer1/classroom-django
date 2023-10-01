const app = new Vue({
    el: '#app',
    delimiters: ["[[", "]]"],  
    data() {
        return {
            edit: false
        }
    },
    methods: {
        ToggleEdit(evt){
            evt.preventDefault()
            this.edit = !this.edit
        },
        Copy(evt){
            evt.preventDefault()
            invite_link = document.querySelector('#invite-link')
            invite_link.select();
            document.execCommand("copy");
        }
    },
})