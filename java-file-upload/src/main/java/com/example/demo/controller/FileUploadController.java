package com.example.demo.controller;

import com.example.demo.service.FileStorageService;
import com.example.demo.dto.MetadataDTO;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.media.Content;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;
import java.io.IOException;
import java.util.Map;

@RestController
@RequestMapping("/api/files")
@Tag(name = "/api/files", description = "Upload a File and Metadata")
public class FileUploadController {

    private final FileStorageService storageService;

    public FileUploadController(FileStorageService storageService) {
        this.storageService = storageService;
    }

    @Operation(summary = "Upload a Document for Processing", description = "Simple Upload Function")
    @ApiResponse(responseCode = "200", description = "Success Upload", content = @Content(mediaType = "application/json"))
    @PostMapping(path = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> uploadFile(
            @RequestPart("file") MultipartFile file,
            @Valid @RequestPart(value = "metadata", required = false) String metadataJson) {
        try {

            if (metadataJson == null || metadataJson.isBlank()) {
                throw new IllegalArgumentException("ERROR-0101:Missing Metadata");
            }

            String storedFileName = storageService.storeFile(file, metadataJson);

            return ResponseEntity.status(HttpStatus.CREATED)
                    .body(Map.of(
                            "fileName", storedFileName,
                            "originalFileName", file.getOriginalFilename(),
                            "size", file.getSize(),
                            "contentType", file.getContentType(),
                            "metadata", metadataJson));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        } catch (IOException e) {
            return ResponseEntity.internalServerError().body(Map.of("error", "Could not store file"));
        }
    }
}
