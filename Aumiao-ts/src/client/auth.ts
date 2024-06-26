
export interface AuthProvider {
    login(): Promise<any>;
    isLogin(): Promise<boolean>;
}

