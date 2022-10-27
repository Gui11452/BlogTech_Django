(function main(){

    const divOculta = document.querySelector('.div-oculta');
    const botao = document.querySelector('.botao-oculto');
    const botaoSpan = document.querySelectorAll('.botao-oculto span');
    const [a,b,c] = botaoSpan;
    const seta = document.querySelector('.seta');

    document.addEventListener('click', e => {

        const el = e.target;

        if(el == botao || el == a || el == b || el == c){

            divOculta.classList.toggle('mostrar-cabecalho-oculto');
            a.classList.toggle('spanOculto1');
            b.classList.toggle('spanOculto2');
            c.classList.toggle('spanOculto3');

        }

        if(el == seta){
            scroll({
                top: 0,
                behavior: 'smooth'
            })
        }

    })

})();