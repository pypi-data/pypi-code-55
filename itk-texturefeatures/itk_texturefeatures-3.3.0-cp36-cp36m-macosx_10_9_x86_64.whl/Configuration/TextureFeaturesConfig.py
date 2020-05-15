depends = ('ITKPyBase', 'ITKStatistics', 'ITKMathematicalMorphology', 'ITKImageGrid', 'ITKCommon', )
templates = (
  ('FixedArray', 'itk::FixedArray', 'itkFixedArrayF8', False, 'float,8'),
  ('Vector', 'itk::Vector', 'itkVectorF8', False, 'float,8'),
  ('Image', 'itk::Image', 'itkImageVF82', False, 'itk::Vector<float,8>,2'),
  ('vector', 'std::vector', 'vectoritkImageVF82', False, 'itk::Image< itk::Vector<float,8>,2  > '),
  ('Image', 'itk::Image', 'itkImageVF83', False, 'itk::Vector<float,8>,3'),
  ('vector', 'std::vector', 'vectoritkImageVF83', False, 'itk::Image< itk::Vector<float,8>,3  > '),
  ('ImageSource', 'itk::ImageSource', 'itkImageSourceIVF82', False, 'itk::Image<itk::Vector<float,8>,2>'),
  ('ImageSource', 'itk::ImageSource', 'itkImageSourceIVF83', False, 'itk::Image<itk::Vector<float,8>,3>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterISS2IVF82', False, 'itk::Image< signed short,2 >, itk::Image<itk::Vector<float,8>,2>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIUC2IVF82', False, 'itk::Image< unsigned char,2 >, itk::Image<itk::Vector<float,8>,2>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIUS2IVF82', False, 'itk::Image< unsigned short,2 >, itk::Image<itk::Vector<float,8>,2>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIF2IVF82', False, 'itk::Image< float,2 >, itk::Image<itk::Vector<float,8>,2>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterID2IVF82', False, 'itk::Image< double,2 >, itk::Image<itk::Vector<float,8>,2>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterISS3IVF83', False, 'itk::Image< signed short,3 >, itk::Image<itk::Vector<float,8>,3>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIUC3IVF83', False, 'itk::Image< unsigned char,3 >, itk::Image<itk::Vector<float,8>,3>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIUS3IVF83', False, 'itk::Image< unsigned short,3 >, itk::Image<itk::Vector<float,8>,3>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIF3IVF83', False, 'itk::Image< float,3 >, itk::Image<itk::Vector<float,8>,3>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterID3IVF83', False, 'itk::Image< double,3 >, itk::Image<itk::Vector<float,8>,3>'),
  ('ImageFileReader', 'itk::ImageFileReader', 'itkImageFileReaderIVF82', False, 'itk::Image<itk::Vector<float,8>,2>'),
  ('ImageFileReader', 'itk::ImageFileReader', 'itkImageFileReaderIVF83', False, 'itk::Image<itk::Vector<float,8>,3>'),
  ('ImageFileWriter', 'itk::ImageFileWriter', 'itkImageFileWriterIVF82', False, 'itk::Image<itk::Vector<float,8>,2>'),
  ('ImageFileWriter', 'itk::ImageFileWriter', 'itkImageFileWriterIVF83', False, 'itk::Image<itk::Vector<float,8>,3>'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterISS2VIF2', True, 'itk::Image< signed short,2 >, itk::VectorImage< float,2 >'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterISS2IVF82', True, 'itk::Image< signed short,2 >, itk::Image<itk::Vector<float,8>,2>'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIUC2VIF2', True, 'itk::Image< unsigned char,2 >, itk::VectorImage< float,2 >'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIUC2IVF82', True, 'itk::Image< unsigned char,2 >, itk::Image<itk::Vector<float,8>,2>'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIUS2VIF2', True, 'itk::Image< unsigned short,2 >, itk::VectorImage< float,2 >'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIUS2IVF82', True, 'itk::Image< unsigned short,2 >, itk::Image<itk::Vector<float,8>,2>'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIF2VIF2', True, 'itk::Image< float,2 >, itk::VectorImage< float,2 >'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIF2IVF82', True, 'itk::Image< float,2 >, itk::Image<itk::Vector<float,8>,2>'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterID2VIF2', True, 'itk::Image< double,2 >, itk::VectorImage< float,2 >'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterID2IVF82', True, 'itk::Image< double,2 >, itk::Image<itk::Vector<float,8>,2>'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterISS3VIF3', True, 'itk::Image< signed short,3 >, itk::VectorImage< float,3 >'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterISS3IVF83', True, 'itk::Image< signed short,3 >, itk::Image<itk::Vector<float,8>,3>'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIUC3VIF3', True, 'itk::Image< unsigned char,3 >, itk::VectorImage< float,3 >'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIUC3IVF83', True, 'itk::Image< unsigned char,3 >, itk::Image<itk::Vector<float,8>,3>'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIUS3VIF3', True, 'itk::Image< unsigned short,3 >, itk::VectorImage< float,3 >'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIUS3IVF83', True, 'itk::Image< unsigned short,3 >, itk::Image<itk::Vector<float,8>,3>'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIF3VIF3', True, 'itk::Image< float,3 >, itk::VectorImage< float,3 >'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterIF3IVF83', True, 'itk::Image< float,3 >, itk::Image<itk::Vector<float,8>,3>'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterID3VIF3', True, 'itk::Image< double,3 >, itk::VectorImage< float,3 >'),
  ('CoocurrenceTextureFeaturesImageFilter', 'itk::Statistics::CoocurrenceTextureFeaturesImageFilter', 'itkCoocurrenceTextureFeaturesImageFilterID3IVF83', True, 'itk::Image< double,3 >, itk::Image<itk::Vector<float,8>,3>'),
  ('FixedArray', 'itk::FixedArray', 'itkFixedArrayF10', False, 'float,10'),
  ('Vector', 'itk::Vector', 'itkVectorF10', False, 'float,10'),
  ('Image', 'itk::Image', 'itkImageVF102', False, 'itk::Vector<float,10>,2'),
  ('vector', 'std::vector', 'vectoritkImageVF102', False, 'itk::Image< itk::Vector<float,10>,2  > '),
  ('Image', 'itk::Image', 'itkImageVF103', False, 'itk::Vector<float,10>,3'),
  ('vector', 'std::vector', 'vectoritkImageVF103', False, 'itk::Image< itk::Vector<float,10>,3  > '),
  ('ImageSource', 'itk::ImageSource', 'itkImageSourceIVF102', False, 'itk::Image< itk::Vector<float,10>,2 >'),
  ('ImageSource', 'itk::ImageSource', 'itkImageSourceIVF103', False, 'itk::Image< itk::Vector<float,10>,3 >'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterISS2IVF102', False, 'itk::Image< signed short,2 >, itk::Image<itk::Vector<float,10>,2>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIUC2IVF102', False, 'itk::Image< unsigned char,2 >, itk::Image<itk::Vector<float,10>,2>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIUS2IVF102', False, 'itk::Image< unsigned short,2 >, itk::Image<itk::Vector<float,10>,2>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIF2IVF102', False, 'itk::Image< float,2 >, itk::Image<itk::Vector<float,10>,2>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterID2IVF102', False, 'itk::Image< double,2 >, itk::Image<itk::Vector<float,10>,2>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterISS3IVF103', False, 'itk::Image< signed short,3 >, itk::Image<itk::Vector<float,10>,3>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIUC3IVF103', False, 'itk::Image< unsigned char,3 >, itk::Image<itk::Vector<float,10>,3>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIUS3IVF103', False, 'itk::Image< unsigned short,3 >, itk::Image<itk::Vector<float,10>,3>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterIF3IVF103', False, 'itk::Image< float,3 >, itk::Image<itk::Vector<float,10>,3>'),
  ('ImageToImageFilter', 'itk::ImageToImageFilter', 'itkImageToImageFilterID3IVF103', False, 'itk::Image< double,3 >, itk::Image<itk::Vector<float,10>,3>'),
  ('ImageFileReader', 'itk::ImageFileReader', 'itkImageFileReaderIVF102', False, 'itk::Image<itk::Vector<float,10>,2>'),
  ('ImageFileReader', 'itk::ImageFileReader', 'itkImageFileReaderIVF103', False, 'itk::Image<itk::Vector<float,10>,3>'),
  ('ImageFileWriter', 'itk::ImageFileWriter', 'itkImageFileWriterIVF102', False, 'itk::Image<itk::Vector<float,10>,2>'),
  ('ImageFileWriter', 'itk::ImageFileWriter', 'itkImageFileWriterIVF103', False, 'itk::Image<itk::Vector<float,10>,3>'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterISS2VIF2', True, 'itk::Image< signed short,2 >, itk::VectorImage< float,2 >'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterISS2IVF102', True, 'itk::Image< signed short,2 >, itk::Image<itk::Vector<float,10>,2>'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIUC2VIF2', True, 'itk::Image< unsigned char,2 >, itk::VectorImage< float,2 >'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIUC2IVF102', True, 'itk::Image< unsigned char,2 >, itk::Image<itk::Vector<float,10>,2>'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIUS2VIF2', True, 'itk::Image< unsigned short,2 >, itk::VectorImage< float,2 >'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIUS2IVF102', True, 'itk::Image< unsigned short,2 >, itk::Image<itk::Vector<float,10>,2>'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIF2VIF2', True, 'itk::Image< float,2 >, itk::VectorImage< float,2 >'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIF2IVF102', True, 'itk::Image< float,2 >, itk::Image<itk::Vector<float,10>,2>'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterID2VIF2', True, 'itk::Image< double,2 >, itk::VectorImage< float,2 >'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterID2IVF102', True, 'itk::Image< double,2 >, itk::Image<itk::Vector<float,10>,2>'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterISS3VIF3', True, 'itk::Image< signed short,3 >, itk::VectorImage< float,3 >'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterISS3IVF103', True, 'itk::Image< signed short,3 >, itk::Image<itk::Vector<float,10>,3>'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIUC3VIF3', True, 'itk::Image< unsigned char,3 >, itk::VectorImage< float,3 >'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIUC3IVF103', True, 'itk::Image< unsigned char,3 >, itk::Image<itk::Vector<float,10>,3>'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIUS3VIF3', True, 'itk::Image< unsigned short,3 >, itk::VectorImage< float,3 >'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIUS3IVF103', True, 'itk::Image< unsigned short,3 >, itk::Image<itk::Vector<float,10>,3>'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIF3VIF3', True, 'itk::Image< float,3 >, itk::VectorImage< float,3 >'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterIF3IVF103', True, 'itk::Image< float,3 >, itk::Image<itk::Vector<float,10>,3>'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterID3VIF3', True, 'itk::Image< double,3 >, itk::VectorImage< float,3 >'),
  ('RunLengthTextureFeaturesImageFilter', 'itk::Statistics::RunLengthTextureFeaturesImageFilter', 'itkRunLengthTextureFeaturesImageFilterID3IVF103', True, 'itk::Image< double,3 >, itk::Image<itk::Vector<float,10>,3>'),
)
snake_case_functions = ('image_file_writer', 'run_length_texture_features_image_filter', 'coocurrence_texture_features_image_filter', 'image_to_image_filter', 'image_file_reader', 'image_source', )
