export const getPlayers = async () => {
  const response = await fetch("https://ajds9c8ox7.execute-api.eu-central-1.amazonaws.com/dev/players", {
    mode: 'cors'});
  const ret = await response.json();
  return ret.players;
}

export const createPlayer = async (body) => {
  const response = await fetch("https://ajds9c8ox7.execute-api.eu-central-1.amazonaws.com/dev/players", {
    method: 'POST',
    body: JSON.stringify(body),
    mode: 'cors'});
  console.log(response);
}