new Vue({
  el: "#app",
  data() {
    return {
      jogos: null,
      jogo: {
        id: null,
        titulo: null,
        genero: null,
        classificacao: null,
        plataforma: null,
      },
      filtro: "",
      erros: [],
    };
  },
  mounted() {
    this.listar();
  },
  methods: {
    listar() {
      axios
        .get("http://127.0.0.1:5000/jogos")
        .then((response) => (this.jogos = response.data));
      this.filtro = "";
    },

    salvar() {
      if (!this.verificaForm()) {
        return;
      }
      if (this.jogo.id) {
        axios
          .put(`http://127.0.0.1:5000/jogos/${this.jogo.id}`, this.jogo)
          .then((response) => {
            alert(`Ok! Jogo Alterado com Sucesso!!`);
            this.listar();
          });
      } else {
        axios
          .post("http://127.0.0.1:5000/jogos", this.jogo)
          .then((response) => {
            alert(`Ok! Jogo Cadastrado com Código: ${response.data.id}`);
            this.listar();
          });
      }
      this.jogo = {};
    },

    editar(id) {
      axios
        .get("http://127.0.0.1:5000/jogos/" + id)
        .then((response) => (this.jogo = response.data));
      this.$refs.titulo.focus();
    },

    excluir(id, titulo) {
      if (confirm(`Confirma exclusão do jogo '${titulo}'?`)) {
        axios.delete("http://127.0.0.1:5000/jogos/" + id).then((response) => {
          alert(`Ok! Jogo '${titulo}' excluído com sucesso!`);
          this.listar();
        });
      }
    },

    pesquisar() {
      if (this.filtro.length == 0) {
        this.listar();
      } else {
        axios
          .get(`http://127.0.0.1:5000/jogos/pesq/${this.filtro}`)
          .then((response) => (this.jogos = response.data));
      }
    },

    verificaForm() {
      // limpa vetor de erros
      this.erros = [];
      if (
        this.jogo.titulo &&
        this.jogo.genero &&
        this.jogo.classificacao &&
        this.jogo.plataforma
      ) {
        return true;
      }

      if (!this.filme.titulo) {
        this.erros.push("Título do jogo é obrigatório.");
      }
      if (!this.filme.genero) {
        this.erros.push("Gênero é obrigatório.");
      }
      if (!this.filme.classificacao) {
        this.erros.push("Classificação do jogo é obrigatório.");
      }
      if (!this.filme.plataforma) {
        this.erros.push("Plataforma é obrigatória.");
      }
      return false;
    },
  },
});