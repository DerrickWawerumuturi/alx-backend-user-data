import request from "request"

const movieId = process.argv[2]
if (!movieId) {
    console.log('Usage: node star_wars_characters.js <Movie ID>');
    process.exit(1)
}

const apiUrl = `https://swapi.dev/api/films/${movieId}/`
request(apiUrl, (error, response, body) => {
    if (error) {
        console.log('Error fetching movie:', error)
        return;
    }

    const movie = JSON.parse(body)
    if (!movie.characters) {
        console.log('No characters found in this movie')
        return;
    }

    movie.characters.forEach((charactersUrl) => {
        request(charactersUrl, (charError, charResponse, charBody) => {
            if (charError) {
                console.error('Error fetching character:', charError)
            }

            const character = JSON.parse(charBody)
            console.log(character.name)
        })
    });
})
