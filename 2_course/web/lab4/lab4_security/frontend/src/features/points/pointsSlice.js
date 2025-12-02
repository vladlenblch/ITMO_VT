import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import pointsApi from '../../services/pointsApi';

export const fetchResults = createAsyncThunk(
    'points/fetchResults',
    async (_, { rejectWithValue }) => {
        try {
            const { data } = await pointsApi.fetchResults();
            return data;
        } catch (error) {
            const message = error.response?.data?.message || 'Не удалось загрузить результаты';
            return rejectWithValue(message);
        }
    },
);

export const submitPoint = createAsyncThunk(
    'points/submitPoint',
    async (payload, { rejectWithValue }) => {
        try {
            const { data } = await pointsApi.submitPoint(payload);
            return data;
        } catch (error) {
            const message = error.response?.data?.message || 'Не удалось проверить точку';
            return rejectWithValue(message);
        }
    },
);

const pointsSlice = createSlice({
    name: 'points',
    initialState: {
        items: [],
        status: 'idle',
        error: null,
        submissionStatus: 'idle',
        currentRadius: 1,
    },
    reducers: {
        clearPoints(state) {
            state.items = [];
            state.error = null;
        },
        setRadius(state, action) {
            state.currentRadius = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchResults.pending, (state) => {
                state.status = 'loading';
                state.error = null;
            })
            .addCase(fetchResults.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.items = action.payload;
            })
            .addCase(fetchResults.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.payload;
            })
            .addCase(submitPoint.pending, (state) => {
                state.submissionStatus = 'loading';
                state.error = null;
            })
            .addCase(submitPoint.fulfilled, (state, action) => {
                state.submissionStatus = 'succeeded';
                state.items = [action.payload, ...state.items];
            })
            .addCase(submitPoint.rejected, (state, action) => {
                state.submissionStatus = 'failed';
                state.error = action.payload;
            });
    },
});

export const { clearPoints, setRadius } = pointsSlice.actions;
export default pointsSlice.reducer;
