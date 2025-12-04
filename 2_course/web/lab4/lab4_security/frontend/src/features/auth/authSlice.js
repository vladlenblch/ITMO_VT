import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import authApi from '../../services/authApi';

const tokenFromStorage = localStorage.getItem('authToken');

export const login = createAsyncThunk(
    'auth/login',
    async (credentials, { rejectWithValue }) => {
        try {
            const { data } = await authApi.login(credentials);
            return data;
        } catch (error) {
            const message = error.response?.data?.message || 'Не удалось выполнить вход';
            return rejectWithValue(message);
        }
    },
);

export const register = createAsyncThunk(
    'auth/register',
    async (credentials, { rejectWithValue }) => {
        try {
            const { data } = await authApi.register(credentials);
            return data;
        } catch (error) {
            const message = error.response?.data?.message || 'Не удалось создать аккаунт';
            return rejectWithValue(message);
        }
    },
);

export const logout = createAsyncThunk('auth/logout', async (_, { rejectWithValue }) => {
    try {
        await authApi.logout();
    } catch (error) {
        const message = error.response?.data?.message || 'Ошибка при выходе из системы';
        return rejectWithValue(message);
    }
});

export const fetchCurrentUser = createAsyncThunk(
    'auth/me',
    async (_, { rejectWithValue }) => {
        try {
            const { data } = await authApi.me();
            return { user: data };
        } catch (error) {
            const message = error.response?.data?.message || 'Не удалось получить данные пользователя';
            return rejectWithValue(message);
        }
    },
);

export const listCredentials = createAsyncThunk(
    'auth/listCredentials',
    async (_, { rejectWithValue }) => {
        try {
            const { data } = await authApi.listCredentials();
            return data;
        } catch (error) {
            const message = error.response?.data?.message || 'Не удалось получить способы входа';
            return rejectWithValue(message);
        }
    },
);

export const deleteCredential = createAsyncThunk(
    'auth/deleteCredential',
    async (id, { rejectWithValue }) => {
        try {
            await authApi.deleteCredential(id);
            return id;
        } catch (error) {
            const message = error.response?.data?.message || 'Не удалось удалить способ входа';
            return rejectWithValue(message);
        }
    },
);

const authSlice = createSlice({
    name: 'auth',
    initialState: {
        user: null,
        token: tokenFromStorage,
        status: 'idle',
        error: null,
        recoveryCodes: [],
        credentials: [],
        ownershipFilePath: null,
        ownershipFileContent: null,
    },
    reducers: {
        clearAuthState(state) {
            state.user = null;
            state.token = null;
            state.status = 'idle';
            state.error = null;
            state.recoveryCodes = [];
            state.credentials = [];
            state.ownershipFilePath = null;
            state.ownershipFileContent = null;
            localStorage.removeItem('authToken');
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(register.pending, (state) => {
                state.status = 'loading';
                state.error = null;
            })
            .addCase(register.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.user = action.payload.user;
                state.token = action.payload.token;
                state.recoveryCodes = action.payload.recoveryCodes || [];
                state.ownershipFilePath = action.payload.ownershipFilePath || null;
                state.ownershipFileContent = action.payload.ownershipFileContent || null;
                localStorage.setItem('authToken', action.payload.token);
            })
            .addCase(register.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.payload;
            })
            .addCase(login.pending, (state) => {
                state.status = 'loading';
                state.error = null;
            })
            .addCase(login.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.user = action.payload.user;
                state.token = action.payload.token;
                localStorage.setItem('authToken', action.payload.token);
            })
            .addCase(login.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.payload;
            })
            .addCase(logout.fulfilled, (state) => {
                state.user = null;
                state.token = null;
                state.status = 'idle';
                localStorage.removeItem('authToken');
            })
            .addCase(logout.rejected, (state, action) => {
                state.error = action.payload;
            })
            .addCase(fetchCurrentUser.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(fetchCurrentUser.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.user = action.payload.user;
            })
            .addCase(fetchCurrentUser.rejected, (state) => {
                state.user = null;
                state.token = null;
                state.status = 'idle';
                localStorage.removeItem('authToken');
            })
            .addCase(listCredentials.fulfilled, (state, action) => {
                state.credentials = action.payload;
            })
            .addCase(deleteCredential.fulfilled, (state, action) => {
                state.credentials = state.credentials.filter((item) => item.id !== action.payload);
            });
    },
});

export const { clearAuthState } = authSlice.actions;
export default authSlice.reducer;
