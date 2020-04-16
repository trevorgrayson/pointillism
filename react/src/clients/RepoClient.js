import React from 'react';

class RepoClient {
    getRepos() { return fetch('/v1/repos').then(result => result.json()) }
}

export default RepoClient;