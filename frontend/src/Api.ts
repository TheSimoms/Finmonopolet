export class ApiResponse {
    count: number;
    next: string;
    previous: string;
    results: ApiProduct[];
};

export class ApiProduct {
    product_number: number;
    name: string;
};
