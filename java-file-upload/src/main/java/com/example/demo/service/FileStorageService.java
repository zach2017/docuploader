package com.example.demo.service;

import com.example.demo.config.StorageProperties;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.*;
import java.time.Instant;
import java.util.UUID;

@Service
public class FileStorageService {

    private final Path basePath;
    private final String keyInfo;

    public FileStorageService(StorageProperties properties) {
        this.basePath = Paths.get(properties.basePath()).toAbsolutePath().normalize();
        this.keyInfo = properties.keyInfo();

        try {
            Files.createDirectories(this.basePath);
        } catch (IOException e) {
            throw new RuntimeException("Could not create upload directory: " + basePath, e);
        }
    }

    public String storeFile(MultipartFile file, String metadataJson) throws IOException {
        if (file.isEmpty()) {
            throw new IllegalArgumentException("Cannot store empty file");
        }

        String originalFilename = StringUtils.cleanPath(file.getOriginalFilename());
        String extension = "";

        int dotIndex = originalFilename.lastIndexOf('.');
        if (dotIndex != -1) {
            extension = originalFilename.substring(dotIndex);
        }

        String storedFileName = "%s_%d%s".formatted(UUID.randomUUID(), Instant.now().toEpochMilli(), extension);
        Path targetLocation = this.basePath.resolve(storedFileName);

        file.transferTo(targetLocation);

        if (metadataJson != null && !metadataJson.isBlank()) {
            Path metaFile = this.basePath.resolve(storedFileName + ".meta.json");
            Files.writeString(metaFile, metadataJson, StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
        }

        return storedFileName;
    }
}
