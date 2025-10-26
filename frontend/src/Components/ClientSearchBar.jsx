import { FaSearch } from "react-icons/fa";

const ClientSearchBar = ({ searchTerm, onSearch }) => {
  const handleChange = (e) => {
    onSearch(e.target.value);
  };

  return (
    <div className="flex items-center justify-between bg-white shadow-md rounded-xl px-4 py-2 mb-4">
      <input
        type="text"
        placeholder="Buscar cliente por nombre o cédula..."
        value={searchTerm}
        onChange={handleChange}
        className="flex-1 outline-none text-gray-700 placeholder-gray-400 bg-transparent px-2"
      />
      <button
        onClick={() => onSearch(searchTerm)}
        className="bg-purple-600 hover:bg-purple-700 text-white p-2 rounded-lg transition-colors"
      >
        <FaSearch />
      </button>
    </div>
  );
};

export default ClientSearchBar;
