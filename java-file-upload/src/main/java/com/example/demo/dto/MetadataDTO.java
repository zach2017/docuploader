package com.example.demo.dto;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public class MetadataDTO {
    @NotNull(message = "Metadata cannot be null")
    @Size(min = 2, max = 256, message = "Meta Data is Required")
    private String data;

    public String getData() { 
        return data;
    }
    // getters/setters
}