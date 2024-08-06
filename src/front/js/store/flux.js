const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			// Variables donde están los arrays vacíos que almacenarán los datos obtenidos de la API.
			vehiculos: [], 
			planetas: [], 
			personajes: [], 
			favoritos: [],
			detalles: {}, // siempre va a ser uno, por eso ponemos {}
			usuario_id: 1 // Ajusta este valor según tu lógica, aquí se asume un ID de usuario de ejemplo
		},

		actions: {
			// Funciones para obtener datos de la API
			obtenerPersonajes: () => {
				fetch("https://www.swapi.tech/api/people", {
					method: "GET" // Obtener la lista de personajes
				})
				.then(response => response.json()) // Convierte la respuesta a formato JSON, formato texto
				.then(data => setStore({ personajes: data.results })) // Actualizar el estado del store personajes
				.catch(error => console.error("Error al recibir los datos de los personajes:", error));
			},

			obtenerVehiculos: () => {
				fetch("https://www.swapi.tech/api/vehicles", {
					method: "GET" // Obtener la lista de vehículos
				})
				.then(response => response.json())
				.then(data => setStore({ vehiculos: data.results })) // Actualizar el estado del store vehículos
				.catch(error => console.error("Error al recibir los datos de los vehículos:", error));
			},

			obtenerPlanetas: () => {
				fetch("https://www.swapi.tech/api/planets", {
					method: "GET" // Obtener la lista de planetas
				})
				.then(response => response.json())
				.then(data => setStore({ planetas: data.results })) // Actualizar el estado del store planetas
				.catch(error => console.error("Error al recibir los datos de los planetas:", error));
			},

			obtenerDetalles: (type, id) => {
				fetch(`https://www.swapi.tech/api/${type}/${id}`, { // por ejemplo https://www.swapi.tech/api/people/1
					method: "GET" // Obtener la lista de personajes, vehículos o planetas de forma individual
				})
				.then(response => response.json()) // Convierte la respuesta a formato JSON, formato texto 
				.then(data => {
					if (data.result) {
						const { properties, description } = data.result;
						setStore({ detalles: { ...properties, description } }); // Actualiza el estado del store del objeto detalles, que contiene todas las propiedades de properties más una nueva propiedad description.
					}
				})
				.catch(error => console.error("Error al recibir los datos de los personajes:", error));
			},

			agregarFavorito: (id, name, type) => {
				const { favoritos, usuario_id } = getStore(); // Obtener el array de favoritos del estado actual y el ID del usuario

				const favoritoExistente = favoritos.find(favorito => favorito.id === id);

				// Verifica si el favorito ya existe en la lista
				if (!favoritoExistente) {
					setStore({ favoritos: [...favoritos, { id, name, type }] });

					// Enviar al backend
					fetch(`/activar_favorito/${usuario_id}`, { // Hacer una solicitud fetch al backend utilizando el método POST
						method: "POST",
						headers: {
							"Content-Type": "application/json"
						},
						body: JSON.stringify({
							usuario_id,
							vehiculo_id: type === 'vehicles' ? id : null,
							personaje_id: type === 'people' ? id : null,
							planeta_id: type === 'planets' ? id : null
						})
					})
					.then(response => response.json())
					.then(data => console.log("Favorito agregado:", data))
					.catch(error => console.error("Error al agregar favorito:", error));
				} else {
					console.warn(`El favorito con ID ${id} ya está en la lista.`); // Esta es una función de la consola del navegador que muestra un mensaje de advertencia. 
				}
			},

			eliminarFavorito: (id) => {
				const { favoritos, usuario_id } = getStore(); // Obtener el array de favoritos del estado actual y el ID del usuario

				// Filtra el ID del favorito a eliminar del array de favoritos
				const nuevosFavoritos = favoritos.filter(favorito => favorito.id !== id); // filter se usa para crear un nuevo array (nuevosFavoritos) que excluye el ID que se quiere eliminar (id).
				setStore({ favoritos: nuevosFavoritos }); // Actualiza el estado global favoritos con el nuevo array nuevosFavoritos, eliminando así el favorito localmente de la lista.
				console.log(nuevosFavoritos)

				// Enviar al backend
				fetch(`/desactivar_favorito/${usuario_id}`, {
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						usuario_id,
						vehiculo_id: id,
						personaje_id: id,
						planeta_id: id
					})
				})
				.then(response => response.json())
				.then(data => console.log('Favorito eliminado:', data))
				.catch(error => console.error('Error al eliminar favorito:', error));
			}
		}
	};
};

export default getState;
