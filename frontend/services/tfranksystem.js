const fetchFromAPI = async (
  route,
  method = 'GET',
  body = null,
  token = null,
) => {
  const mode = 'cors';

  const options = {
    method,
    mode,
    ...(body ? { body } : {}),
  };

  return await fetch(`${process.env.API_URL}/${route}`, options);
};

export const getPlayers = async () => {
  const response = await fetchFromAPI('players');
  const ret = await response.json();
  return ret.players;
};

export const getMatches = async () => {
  const response = await fetchFromAPI('matches');
  const ret = await response.json();
  return ret.matches;
};

export const createPlayer = async body => {
  return await fetchFromAPI('players', 'POST', JSON.stringify(body));
};

export const createMatch = async body => {
  return await fetchFromAPI('matches', 'POST', JSON.stringify(body));
};

export const authenticate = async (username, password) => {
  const body = { username, password };
  const response = await fetchFromAPI(
    'oauth/token',
    'POST',
    JSON.stringify(body),
  );

  if (response.status != 200) {
    return false;
  }

  const ret = await response.json();
  return ret.token;
};
