Vue.component('answer-component', 
{ 
    delimiters: ["[[", "]]"],   
    props: {
        number: Number,
        questionNumber: Number,
        readonly: Boolean,
    },
    template:'<li class="test-creation-from__item__answer" @click="Select"><input :name="[[SetName()]]" :readonly="readonly" required></li>',
    methods:{
        SetName(){
            return `answer_${this.questionNumber}_${this.number}`
        },
        Select(evt){
            if (evt.target.readOnly){
                let class_ = 'test-creation-from--right'
                let add = false
                if (!evt.target.classList.contains(class_)){
                    evt.target.classList.add(class_)
                    add = true
                }
                else{
                    evt.target.classList.remove(class_)
                }
                this.$emit('select', {
                    number: this.number,
                    add : add,
                  })
            }
        }
    }
})


Vue.component('question-component', { 
    data(){
        return{
            answerCount: 4,
            answersDisabled: false,
            correctAnswers: []
        }
    },
    delimiters: ["[[", "]]"],   
    methods: {
        addAnswer(evt){
            evt.preventDefault()
            this.answerCount < 8 ? this.answerCount += 1 : null
        },
        removeAnswer(evt){
            evt.preventDefault()
            if (this.answerCount > 2){
                let index = this.correctAnswers.indexOf(this.answerCount)
                if (index != -1){
                    this.Select({number:this.answerCount, add:false})
                }
                this.answerCount -= 1 }

            
        },
        toggleDisabled(evt){
            evt.preventDefault()
            this.answersDisabled = !this.answersDisabled
        },
        Select(data){
            if (data.add){
                this.correctAnswers.push(data.number)
            }
            else{
                let index = this.correctAnswers.indexOf(data.number)
                this.correctAnswers.splice(index, 1)
            }
            console.log(this.correctAnswers)
            console.log(data)
        },
      
        RemoveQuestion(evt){
            evt.preventDefault()
            this.$emit('remove', {
                id: this.id
              })
        },

        SetAnswersName(){
            return `answers_${this.number}`
        },
        SetQuestionName(){
            return `question_${this.number}`
        }
        
    },

    props:{
        number: Number,
        id: Number,
        value: String
    },
    
    template:
    `
    <div class="form__item test-creation-from__item">
        <div class="test-creation-from__question">
            <label class="test-creation-from__question-title" for="question">Вопрос: [[number]]</label>
            <input class="test-creation-from__question-input" type="input" :name="SetQuestionName()" required>
        </div>
        <ul class="test-creation-from__item__answers">
            <answer-component v-for="i in answerCount" :key="i" :number="i" :readonly="answersDisabled" @select="Select" :questionNumber="number"></answer-component>
        </ul>
        <div class="test-creation-from__question__buttons">
            <button @click="addAnswer" class="button button--add test-creation-from__add">
                <i class="fa-solid fa-plus"></i>
                <!-- <p class="button__text">add</p> -->
            </button>
            <button @click="removeAnswer" class="button button--error test-creation-from__remove">
                <i class="fa-solid fa-xmark"></i>
                <!-- <p class="button__text">remove</p> -->
            </button>
            <button @click="toggleDisabled" class="button button--sucess test-creation-from__select">
                <i class="fa-solid fa-check"></i>
                <!-- <p class="button__text">select right</p> -->
            </button>
        </div>
        <input type="hidden" :name="SetAnswersName()" class="test-creation-from__answers-values" :value="correctAnswers">
    </div>
    `
})



const app = new Vue({
    el: '#app',
    delimiters: ["[[", "]]"],   
    data() {
        return {
            questions: [{id:Date.now()}],
        }
    },
    methods:{
        addQuestion(evt){
            evt.preventDefault()
            this.questions.push({id:Date.now()})
            console.log(this.questions)
        },
        RemoveQuestion(data){
            console.log(data)
            
            let index = this.questions.findIndex(item => item.id === data.id)
            this.questions.splice(index, 1)
            console.log(data.id)
            console.log(index)
            console.log(this.questions)
        }
        
        
    }
})

