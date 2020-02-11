export const getPlayers = async () => {
  const response = await fetch(`${process.env.API_URL}/players`, {
    mode: 'cors'});
  const ret = await response.json();
  return ret.players;
}

export const getMatches = async () => {
  const response = await fetch(`${process.env.API_URL}/matches`, {
    mode: 'cors'});
  const ret = await response.json();
  return ret.matches;
}

export const createPlayer = async (body) => {
  const response = await fetch(`${process.env.API_URL}/players`, {
    method: 'POST',
    body: JSON.stringify(body),
    mode: 'cors'});

  return response;
}

export const createMatch = async (body) => {
  const response = await fetch(`${process.env.API_URL}/matches`, {
    method: 'POST',
    body: JSON.stringify(body),
    mode: 'cors'});

  return response;
}