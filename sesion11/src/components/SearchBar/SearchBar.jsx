import './SearchBar.css'

// Controlled input: the state lives in App, not here
function SearchBar({ value, onChange, isSearching }) {
  return (
    <div className="search-bar">
      <span className="search-bar__icon">🔍</span>
      <input
        type="text"
        placeholder="Buscar por título o género..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
      {isSearching && <span className="search-bar__status">Buscando...</span>}
    </div>
  )
}

export default SearchBar