import './Header.css'

// Receives only the number, never the full favorites list
function Header({ favoritesCount }) {
  return (
    <header className="header">
      <div className="container flex between">
        <div>
          <h1>Cartelera Lab 11</h1>
          <p className="muted">Comunicación entre componentes en React</p>
        </div>

        <div className="header__favorites" title="Películas favoritas">
          <span className="header__heart">♥</span>
          <span>Favoritas</span>
          <span className="header__count">{favoritesCount}</span>
        </div>
      </div>
    </header>
  )
}

export default Header