cmake_minimum_required(VERSION 3.20)
set(LIB_NAME "libarchive")
project(${LIB_NAME} C)

find_library(ZLIB_RELEASE PATHS ${PROJECT_DEPS_INSTALL_PATH} REQUIRED NO_DEFAULT_PATH NAMES "zlibstatic_release" "zlib_release" "zlib_release.dll" PATH_SUFFIXES lib)
find_library(ZLIB_DEBUG PATHS ${PROJECT_DEPS_INSTALL_PATH} REQUIRED NO_DEFAULT_PATH NAMES "zlibstaticd" "zlibstatic_debug" "zlibd" "zlib_debug.dll" PATH_SUFFIXES lib)
message(STATUS "ZLIB_RELEASE ${ZLIB_RELEASE}")
message(STATUS "ZLIB_DEBUG ${ZLIB_DEBUG}")

find_path(LIBARCHIVE_SRC_PATH
NAMES "archive_read.c"
PATHS 
  "${PROJECT_DEPS_PATH}/libarchive/libarchive"
  "${CMAKE_CURRENT_SOURCE_DIR}/../libarchive/libarchive"
NO_DEFAULT_PATH 
REQUIRED)

# Public headers
SET(include_HEADERS
  archive.h
  archive_entry.h
)

# Sources and private headers
SET(libarchive_SOURCES
  archive_acl.c
  archive_acl_private.h
  archive_check_magic.c
  archive_cmdline.c
  archive_cmdline_private.h
  archive_crc32.h
  archive_cryptor.c
  archive_cryptor_private.h
  # archive_digest.c
  # archive_digest_private.h
  archive_endian.h
  archive_entry.c
  archive_entry.h
  archive_entry_copy_stat.c
  archive_entry_link_resolver.c
  archive_entry_locale.h
  archive_entry_private.h
  archive_entry_sparse.c
  archive_entry_stat.c
  archive_entry_strmode.c
  archive_entry_xattr.c
  # archive_getdate.c
  # archive_getdate.h
  archive_hmac.c
  archive_hmac_private.h
  archive_match.c
  archive_openssl_evp_private.h
  archive_openssl_hmac_private.h
  archive_options.c
  archive_options_private.h
  # archive_pack_dev.h
  # archive_pack_dev.c
  # archive_pathmatch.c
  # archive_pathmatch.h
  archive_platform.h
  archive_platform_acl.h
  archive_platform_xattr.h
  archive_ppmd_private.h
  archive_ppmd8.c
  archive_ppmd8_private.h
  # archive_ppmd7.c
  # archive_ppmd7_private.h
  archive_private.h
  archive_random.c
  archive_random_private.h
  archive_rb.c
  archive_rb.h
  archive_read.c
  archive_read_add_passphrase.c
  # archive_read_append_filter.c
  # archive_read_data_into_fd.c
  # archive_read_disk_entry_from_file.c
  # archive_read_disk_posix.c
  # archive_read_disk_private.h
  # archive_read_disk_set_standard_lookup.c
  # archive_read_extract.c
  # archive_read_extract2.c
  archive_read_open_fd.c
  archive_read_open_file.c
  archive_read_open_filename.c
  archive_read_open_memory.c
  archive_read_private.h
  archive_read_set_format.c
  archive_read_set_options.c
  # archive_read_support_filter_by_code.c
  # archive_read_support_filter_bzip2.c
  archive_read_support_filter_compress.c
  # archive_read_support_filter_gzip.c
  # archive_read_support_filter_grzip.c
  # archive_read_support_filter_lrzip.c
  # archive_read_support_filter_lz4.c
  # archive_read_support_filter_lzop.c
  archive_read_support_filter_none.c
  # archive_read_support_filter_program.c
  # archive_read_support_filter_rpm.c
  # archive_read_support_filter_uu.c
  # archive_read_support_filter_xz.c
  # archive_read_support_filter_zstd.c
  # archive_read_support_format_7zip.c
  # archive_read_support_format_ar.c
  # archive_read_support_format_by_code.c
  # archive_read_support_format_cab.c
  # archive_read_support_format_cpio.c
  # archive_read_support_format_empty.c
  # archive_read_support_format_iso9660.c
  # archive_read_support_format_lha.c
  # archive_read_support_format_mtree.c
  # archive_read_support_format_rar.c
  # archive_read_support_format_rar5.c
  # archive_read_support_format_raw.c
  # archive_read_support_format_tar.c
  # archive_read_support_format_warc.c
  # archive_read_support_format_xar.c
  archive_read_support_format_zip.c
  archive_string.c
  archive_string.h
  archive_string_composition.h
  archive_string_sprintf.c
  archive_util.c
  # archive_version_details.c
  archive_virtual.c
  archive_write.c
  # archive_write_disk_posix.c
  # archive_write_disk_private.h
  # archive_write_disk_set_standard_lookup.c
  archive_write_private.h
  archive_write_open_fd.c
  archive_write_open_file.c
  archive_write_open_filename.c
  archive_write_open_memory.c
  # archive_write_add_filter.c
  # archive_write_add_filter_b64encode.c
  # archive_write_add_filter_by_name.c
  # archive_write_add_filter_bzip2.c
  archive_write_add_filter_compress.c
  # archive_write_add_filter_grzip.c
  # archive_write_add_filter_gzip.c
  # archive_write_add_filter_lrzip.c
  # archive_write_add_filter_lz4.c
  # archive_write_add_filter_lzop.c
  archive_write_add_filter_none.c
  # archive_write_add_filter_program.c
  # archive_write_add_filter_uuencode.c
  # archive_write_add_filter_xz.c
  # archive_write_add_filter_zstd.c
  # archive_write_set_format.c
  # archive_write_set_format_7zip.c
  # archive_write_set_format_ar.c
  # archive_write_set_format_by_name.c
  # archive_write_set_format_cpio.c
  # archive_write_set_format_cpio_binary.c
  # archive_write_set_format_cpio_newc.c
  # archive_write_set_format_cpio_odc.c
  # archive_write_set_format_filter_by_ext.c
  # archive_write_set_format_gnutar.c
  # archive_write_set_format_iso9660.c
  # archive_write_set_format_mtree.c
  # archive_write_set_format_pax.c
  archive_write_set_format_private.h
  archive_write_set_format_raw.c
  # archive_write_set_format_shar.c
  # archive_write_set_format_ustar.c
  # archive_write_set_format_v7tar.c
  # archive_write_set_format_warc.c
  # archive_write_set_format_xar.c
  archive_write_set_format_zip.c
  archive_write_set_options.c
  archive_write_set_passphrase.c
  archive_xxhash.h
  # filter_fork_posix.c
  # filter_fork.h
  # xxhash.c
)

IF(WIN32 AND NOT CYGWIN)
  LIST(APPEND libarchive_SOURCES archive_entry_copy_bhfi.c)
  LIST(APPEND libarchive_SOURCES archive_read_disk_windows.c)
  LIST(APPEND libarchive_SOURCES archive_windows.c)
  LIST(APPEND libarchive_SOURCES archive_windows.h)
  LIST(APPEND libarchive_SOURCES archive_write_disk_windows.c)
  LIST(APPEND libarchive_SOURCES filter_fork_windows.c)
ENDIF(WIN32 AND NOT CYGWIN)

# IF(ARCHIVE_BLAKE2)
  LIST(APPEND libarchive_SOURCES archive_blake2sp_ref.c)
  LIST(APPEND libarchive_SOURCES archive_blake2s_ref.c)
# ENDIF(ARCHIVE_BLAKE2)

IF(ARCHIVE_ACL_DARWIN)
  LIST(APPEND libarchive_SOURCES archive_disk_acl_darwin.c)
ELSEIF(ARCHIVE_ACL_FREEBSD)
  LIST(APPEND libarchive_SOURCES archive_disk_acl_freebsd.c)
ELSEIF(ARCHIVE_ACL_LIBACL)
  LIST(APPEND libarchive_SOURCES archive_disk_acl_linux.c)
ELSEIF(ARCHIVE_ACL_SUNOS)
  LIST(APPEND libarchive_SOURCES archive_disk_acl_sunos.c)
ENDIF()

list(TRANSFORM include_HEADERS PREPEND "${LIBARCHIVE_SRC_PATH}/")
list(TRANSFORM libarchive_SOURCES PREPEND "${LIBARCHIVE_SRC_PATH}/")
list(APPEND libarchive_SOURCES 
archive_read_support_filter_all.c
archive_read_support_format_all.c
archive_write_add_filter.c
archive_write_set_format.c
)
add_library(${LIB_NAME})
target_sources(${LIB_NAME} PRIVATE ${libarchive_SOURCES})
target_sources(${LIB_NAME} PUBLIC ${include_HEADERS})
target_include_directories(${LIB_NAME} PRIVATE ${LIBARCHIVE_SRC_PATH})
target_include_directories(${LIB_NAME} PUBLIC ${PROJECT_DEPS_INSTALL_PATH}/include)
target_link_libraries(${LIB_NAME} PUBLIC optimized ${ZLIB_RELEASE} debug ${ZLIB_DEBUG})
set(CONFIG_FILE "config.h")
if (CLANG AND WIN32)
  set(CONFIG_FILE "config-win-clang.h")
endif()
if (MSVC AND WIN32)
  set(CONFIG_FILE "config-win-msvc.h")
endif()
if (CLANG AND LINUX)
  set(CONFIG_FILE "config-linux-clang.h")
endif()

target_compile_definitions(${LIB_NAME} PUBLIC LIBARCHIVE_STATIC PLATFORM_CONFIG_H="${CMAKE_CURRENT_LIST_DIR}/${CONFIG_FILE}" FUNNY=2)
set_source_files_properties(${libarchive_SOURCES} PROPERTIES SKIP_UNITY_BUILD_INCLUSION ON)
include(GNUInstallDirs)
install(TARGETS ${LIB_NAME}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(FILES ${include_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
