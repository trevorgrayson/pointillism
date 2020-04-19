class RepoClient {
    static getRepos() { return fetch('/v1/repos').then(result => result.json()) }
}

export default RepoClient;