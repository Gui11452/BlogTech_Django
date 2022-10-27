(function main(){

    const seta = document.querySelector('.seta');

    document.addEventListener('click', e => {

        const el = e.target;
        if(el == seta){
            scroll({
                top: 0,
                behavior: 'smooth'
            })
        }

    })

})();